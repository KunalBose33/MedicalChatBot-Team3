from pydantic import BaseModel
from typing import Optional

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: Optional[int]
    content: str

class MessageRead(MessageCreate):
    id: int

    class Config:
        orm_mode = True
