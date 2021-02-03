from sqlalchemy import Column, INT, VARCHAR, BOOLEAN, ForeignKey

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    id = Column(INT(), primary_key=True, nullable=False)
    message = Column(VARCHAR(3000), nullable=False)
    sender_id = Column(INT(), ForeignKey('users.id'), nullable=False)
    recipient_id = Column(INT(), ForeignKey('users.id'), nullable=False)
    created_at = Column(VARCHAR(50), nullable=False)
    updated_at = Column(VARCHAR(50), nullable=True)
    is_deleted = Column(BOOLEAN(), nullable=False)