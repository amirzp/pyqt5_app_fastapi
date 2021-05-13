from fastapi import Depends, status, Response, HTTPException
from contact import schemas
from contact import models
from database import database
from sqlalchemy.orm import Session
from app_main import app


# #### get query on database >>
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/contact', status_code=status.HTTP_201_CREATED)
def create_contact(request: schemas.ContactSchemas, db: Session = Depends(get_db)):
    """ساخت مخاطب جدید"""

    # new_contact = models.ContactModel(
    #     name=request.name,
    #     family=request.family,
    #     phone=request.phone,
    #     email=request.email
    # )
    new_contact = models.ContactModel(**request.dict())

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@app.get('/contact', status_code=status.HTTP_200_OK)
def get_contacts(db: Session = Depends(get_db)):
    """برگشت تمام مخاطبین"""

    contacts = db.query(models.ContactModel).all()
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact list is empty')
    return contacts


@app.get('/contact/{_id}', status_code=status.HTTP_200_OK)
def get_contact(_id: int,  response: Response, db: Session = Depends(get_db)):
    """برگشت یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).filter(models.ContactModel.id == _id).first()
    if contact is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Contact with the ID: {_id} not available"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    return contact


@app.delete('/contact/{_id}')
def delete_contact(_id: int, db: Session = Depends(get_db)):
    """پاک کردن یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).get(_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    db.query(models.ContactModel).filter(
        models.ContactModel.id == _id
    ).delete(synchronize_session=False)
    db.commit()

    # headers={"WWW-Authenticate": "Bearer"}


@app.put('/contact/{_id}', status_code=status.HTTP_202_ACCEPTED)
def contact_update(request: schemas.ContactSchemas, _id: int, db: Session = Depends(get_db)):
    """آپدیت یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).get(_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    db.query(models.ContactModel).filter(models.ContactModel.id == _id).update(request.dict())
    db.commit()



