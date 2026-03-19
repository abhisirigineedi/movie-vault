"""SQLAlchemy ORM models for user favorites."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Favorite(Base):
    """Represents a row in the 'favorites' table."""

    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="favorites")
    movie = relationship("DBMovie", backref="user_favorites")

    def __repr__(self) -> str:
        return f"<Favorite(user_id={self.user_id}, movie_id={self.movie_id})>"
