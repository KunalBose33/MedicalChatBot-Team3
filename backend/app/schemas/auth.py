from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str]
    password: str
    role: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str

    class Config:
        orm_mode = True
