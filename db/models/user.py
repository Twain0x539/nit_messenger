from sqlalchemy import VARCHAR, Column, VARBINARY, INT

from db.models import BaseModel


class DBUser(BaseModel):

    __tablename__ = 'users'

    id = Column(INT(), primary_key=True, nullable=False)
    login = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(VARBINARY, nullable=False)
    first_name = Column(VARCHAR(50), nullable=False)
    last_name = Column(VARCHAR(50), nullable=False)
    created_at = Column(VARCHAR(50), nullable= False)
    updated_at = Column(VARCHAR(50))