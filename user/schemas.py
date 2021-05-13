from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchemas(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: Optional[bool]
    is_staff: Optional[bool]
    password: str


class OutUserSchemas(BaseModel):
    class Config:
        orm_mode = True
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: Optional[bool]
    is_staff: Optional[bool]
