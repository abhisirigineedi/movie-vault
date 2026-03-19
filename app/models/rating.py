"""SQLAlchemy ORM models for user-specific ratings."""

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Rating(Base):
    """Represents a row in the 'ratings' table."""

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)

    user = relationship("User", back_populates="ratings")
    movie = relationship("DBMovie", backref="user_ratings")

    def __repr__(self) -> str:
        return f"<Rating(user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating})>"
