"""SQLAlchemy ORM model for the movies table."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class DBMovie(Base):
    """Represents a row in the 'movies' table."""

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=True)
    rating = Column(Float, nullable=True)
    year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<DBMovie(id={self.id}, title='{self.title}')>"
