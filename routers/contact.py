from fastapi import Depends, status, Response
from contact import schemas
from database import database
from sqlalchemy.orm import Session
from contact import repository
from jwt_token import jwt
from user import schemas as user_schemas

from fastapi import APIRouter

router = APIRouter(
    tags=['Contact'],
    prefix='/contact'
)

get_db = database.get_db


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OutContactSchemas
)
def create_contact(
        request: schemas.ContactSchemas,
        db: Session = Depends(get_db),
        current_user: user_schemas.UserSchemas = Depends(
            jwt.get_current_active_user
        )
):
    """ساخت مخاطب جدید"""

    return repository.create(request, db)


@router.get('/', status_code=status.HTTP_200_OK)
def get_contacts(
        db: Session = Depends(get_db),
        current_user: user_schemas.UserSchemas = Depends(
            jwt.get_current_active_user
        )
):
    """برگشت تمام مخاطبین"""

    return repository.get_contacts(db, current_user.id)


@router.get(
    '/{_id}',
    response_model=schemas.OutContactSchemas,
    status_code=status.HTTP_200_OK
)
def get_contact(
        _id: int,
        response: Response,
        db: Session = Depends(get_db),
        current_user: user_schemas.UserSchemas = Depends(
            jwt.get_current_active_user
        )
):
    """برگشت یک مخاطب در صورت وجود"""

    return repository.get_contact(db, current_user.id, _id)


@router.delete('/{_id}')
def delete_contact(
        _id: int,
        db: Session = Depends(get_db),
        current_user: user_schemas.UserSchemas = Depends(
            jwt.get_current_active_user
        )
):
    """پاک کردن یک مخاطب در صورت وجود"""

    return repository.delete(db, current_user.id, _id)


@router.put('/{_id}', status_code=status.HTTP_202_ACCEPTED)
def contact_update(
        request: schemas.ContactSchemas,
        _id: int,
        db: Session = Depends(get_db),
        current_user: user_schemas.UserSchemas = Depends(
            jwt.get_current_active_user
        )
):
    """آپدیت یک مخاطب در صورت وجود"""

    return repository.update(request, db, current_user.id, _id)
