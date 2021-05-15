from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from user import models


# ##### make hash password >>
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
# ## <<


# #### get user in db if user is exist >>
def check_user(user: str, db: Session):
    """چک کردن یوزر در صورت وجود نداشتن برای ساخت یوزر جدید"""

    user = db.query(models.UserModel).filter(models.UserModel.username == user).first()
    if user is None:
        return True
    return False


def create(request, db):
    """ساخت یوزر جدید"""

    flag = check_user(request.username, db)
    if flag is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="the user name is exist")

    request.password = get_password_hash(request.password)
    new_user = models.UserModel(**request.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user(db, _id: int):
    """برگشت یک یورز در صورت وجود"""

    user = db.query(models.UserModel).filter(models.UserModel.id == _id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the ID: {_id} not available"
        )
    return user
