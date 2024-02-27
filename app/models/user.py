from attrs import define
from typing import Optional
from pydantic import BaseModel, EmailStr


@define
class UserCreate:
    email: str
    full_name: str
    password: str
    photo: str

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    photo: str | None = None
