from fastapi import Depends, status
from user import schemas
from database import database
from sqlalchemy.orm import Session
from user import repository

from fastapi import APIRouter

router = APIRouter(
    tags=['User'],
    prefix='/user'
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def post_users(request: schemas.UserSchemas, db: Session = Depends(get_db)):
    """ساخت یوزر جدید"""

    return repository.create(request, db)


@router.get('/{_id}', status_code=status.HTTP_200_OK, response_model=schemas.OutUserSchemas)
def get_user(_id: int, db: Session = Depends(get_db)):
    """برگشت یک یورز در صورت وجود"""

    return repository.get_user(db, _id)
