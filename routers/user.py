from fastapi import Depends, status
from user import schemas
from database import database
from sqlalchemy.orm import Session
from user import repository
from jwt_token import jwt

from fastapi import APIRouter

router = APIRouter(
    tags=['User'],
    prefix='/user'
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def post_users(
    request: schemas.UserPostSchemas,
    db: Session = Depends(get_db)
):
    """ساخت یوزر جدید"""

    return repository.create(request, db)


@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=schemas.OutUserSchemas
)
def get_user(
        current_user: schemas.UserSchemas = Depends(
            jwt.get_current_active_user
        )
):
    """برگشت یک یورز در صورت وجود"""

    return repository.get_user(current_user)


@router.put(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=schemas.OutUserPutSchemas
)
def update(
        request: schemas.OutUserPutSchemas,
        db: Session = Depends(get_db),
        current_user: schemas.UserSchemas = Depends(
            jwt.get_current_active_user
        )
):
    """مدیریت کردن اکانت یوزر"""

    return repository.update(request, db, current_user)
