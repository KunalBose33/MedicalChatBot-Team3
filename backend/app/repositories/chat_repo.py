from sqlalchemy.orm import Session
from app.models.chat import ChatMessage

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, message: ChatMessage):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_for_user(self, user_id: int):
        return self.db.query(ChatMessage).filter(
            (ChatMessage.sender_id == user_id) | (ChatMessage.receiver_id == user_id)
        ).order_by(ChatMessage.created_at).all()
