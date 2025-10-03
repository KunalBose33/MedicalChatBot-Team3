from pydantic import BaseModel

class FileMetaSchema(BaseModel):
    id: int
    user_id: int
    filename: str
    content_type: str

    class Config:
        orm_mode = True
