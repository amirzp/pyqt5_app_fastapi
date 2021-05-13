from fastapi import Depends, status, HTTPException
from user import schemas, models
from database import database
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app_main import app


# ##### make hash password >>
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
# ## <<


# #### get query on database >>
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# #### get user in db if user is exist >>
def check_user(user: str, db: Session):
    """چک کردن یوزر در صورت وجود نداشتن برای ساخت یوزر جدید"""
    user = db.query(models.UserModel).filter(models.UserModel.username == user).first()
    if user is None:
        return True
    return False


@app.post('/user', status_code=status.HTTP_201_CREATED)
def post_users(request: schemas.UserSchemas, db: Session = Depends(get_db)):
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


@app.get('/user/{_id}', status_code=status.HTTP_200_OK, response_model=schemas.OutUserSchemas)
def get_user(_id: int, db: Session = Depends(get_db)):
    """برگشت یک یورز در صورت وجود"""

    user = db.query(models.UserModel).filter(models.UserModel.id == _id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the ID: {_id} not available"
        )
    return user
