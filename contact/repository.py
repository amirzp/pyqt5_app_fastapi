from contact import models
from fastapi import HTTPException, status


def create(request, db):
    """ساخت مخاطب جدید"""

    # new_contact = models.ContactModel(
    #     name=request.name,
    #     family=request.family,
    #     phone=request.phone,
    #     email=request.email,
    #     user=1
    # )
    new_contact = models.ContactModel(**request.dict())

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def get_contacts(db, user_id):
    """برگشت تمام مخاطبین"""

    contacts = db.query(models.ContactModel).filter(
        models.ContactModel.user == user_id
    ).all()

    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Contact list is empty'
        )
    return contacts


def get_contact(db, user_id, _id: int):
    """برگشت یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).filter(
        models.ContactModel.user == user_id
    ).filter(
        models.ContactModel.id == _id
    ).first()
    if contact is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Contact with the ID: {_id} not available"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    return contact


def delete(db, user_id, _id: int):
    """پاک کردن یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).filter(
        models.ContactModel.user == user_id
    ).filter(
        models.ContactModel.id == _id
    ).first()

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    db.query(models.ContactModel).filter(
        models.ContactModel.id == _id
    ).delete(synchronize_session=False)
    db.commit()


def update(request, db, user_id, _id: int):
    """آپدیت یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).filter(
        models.ContactModel.user == user_id
    ).filter(
        models.ContactModel.id == _id
    ).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    db.query(models.ContactModel).filter(
        models.ContactModel.id == _id
    ).update(request.dict())
    db.commit()
    return {'detail': f'Contact with the ID: {_id} is updated.'}
