from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import database
from fastapi.security import OAuth2PasswordRequestForm
from jwt_token import jwt
from user import schemas


router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db


# OAuth2PasswordRequestForm = Depends()
@router.post('/login/', status_code=status.HTTP_200_OK)
def login(request: schemas.OutLoginSchemas, db: Session = Depends(get_db)):
    """لاگین کردن یوزر و دریافت توکن"""

    token = jwt.login(request, db)
    # return JSONResponse(content=token)
    return token
