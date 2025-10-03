from sqlalchemy.orm import Session
from app.models.file import FileMeta

class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_file(self, file: FileMeta):
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def get_files_for_user(self, user_id: int):
        return self.db.query(FileMeta).filter(FileMeta.user_id == user_id).all()

    def get_file_by_id(self, file_id: int):
        return self.db.query(FileMeta).filter(FileMeta.id == file_id).first()
