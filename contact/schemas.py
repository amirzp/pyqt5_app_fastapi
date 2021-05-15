from pydantic import BaseModel, EmailStr
from typing import List
from user.schemas import OutUserSchemas


class ContactSchemas(BaseModel):
    name: str
    family: str
    phone: str
    email: EmailStr
    user: int


class OutContactSchemas(BaseModel):
    class Config:
        orm_mode = True
    id: int
    name: str
    family: str
    phone: str
    email: EmailStr
    user: int
    # owner: OutUserSchemas
