from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import uuid
from app.db.session import Base


def generate_uuid():
    return str(uuid.uuid4()).replace("-", "")

class User(Base):
    __tablename__ = "users"

    id = Column(String(32), primary_key=True, index=True, default=generate_uuid, unique=True)
    name = Column(String(100), index=True)
    email = Column(String(120), unique=True, index=True)
    hashed_password = Column(String(128))

    posts = relationship("Post", back_populates="user")