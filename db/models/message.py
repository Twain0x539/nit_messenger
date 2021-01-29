from sqlalchemy import Column, INT, VARCHAR

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    message = Column(VARCHAR(3000), nullable=False)
    sender_id = Column(INT(), nullable=False)
    recipient_id = Column(INT(), nullable=False)
    created_at = Column(VARCHAR(50), nullable=False)
    updated_at = Column(VARCHAR(50), nullable=True)