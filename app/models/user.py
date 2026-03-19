"""SQLAlchemy ORM models for the User."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """Represents a row in the 'users' table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    ratings = relationship("Rating", back_populates="user", cascade="all, delete")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
