from pydantic import BaseModel
from typing import Optional


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
