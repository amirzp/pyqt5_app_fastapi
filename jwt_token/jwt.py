from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from user import models, repository, schemas
from jwt_token import schemas as jwt_schemas
from database import database
from sqlalchemy.orm import Session


get_db = database.get_db

# openssl rand -hex 32 >> make SECRET_KEY for create access token.
SECRET_KEY = "d913b79da7c38878795f25d8ff425ca17f1026e915a5dff4ae7dff38e6342315"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# #### get user in db if user is exist >>
def check_user(user: str, db: Session):
    """چک کردن یوزر در صورت وجود نداشتن برای ساخت یوزر جدید"""

    user = db.query(models.UserModel).filter(
        models.UserModel.username == user
        ).first()
    if user is None:
        return True
    return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """create access token"""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login(request, db):
    user = db.query(models.UserModel).filter(
        models.UserModel.username == request.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username"
        )
    if not repository.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    # #### give access token from 'create_access_token' function >>
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = jwt_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(models.UserModel).filter(
        models.UserModel.username == token_data.username
    ).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: schemas.UserSchemas = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def read_users_me(
    current_user: schemas.UserSchemas = Depends(get_current_active_user)
):
    return current_user


def update_user_me(
    request,
    db,
    current_user: schemas.UserSchemas = Depends(get_current_active_user)
):
    flag = check_user(request.username, db)
    if flag is False:
        if not current_user.username == request.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="the user name is exist"
            )

    db.query(models.UserModel).filter(
        models.UserModel.id == current_user.id
        ).update(request.dict())
    db.commit()
