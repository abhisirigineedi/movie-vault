"""SQLAlchemy ORM model for the movies table."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class DBMovie(Base):
    """Represents a row in the 'movies' table."""

    __tablename__ = "movies"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True) # Added for user isolation
    title = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=True)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="movies")

    def __repr__(self) -> str:
        return f"<DBMovie(id={self.id}, title='{self.title}')>"
