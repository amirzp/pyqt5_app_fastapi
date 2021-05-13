from pydantic import BaseModel, EmailStr


class ContactSchemas(BaseModel):
    name: str
    family: str
    phone: str
    email: EmailStr
