import uuid

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Boolean, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_activ = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)
