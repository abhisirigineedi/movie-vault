"""Business logic for movie wishlist — SQL database-backed (v1.0)."""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.db_movie import DBMovie


# ---------------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------------

def get_all_movies(db: Session) -> list[DBMovie]:
    """Return every movie, ordered by creation time (newest last)."""
    return db.query(DBMovie).order_by(DBMovie.id.asc()).all()


def get_movie_by_id(db: Session, movie_id: int) -> Optional[DBMovie]:
    """Return a single movie by primary key, or None if not found."""
    return db.query(DBMovie).filter(DBMovie.id == movie_id).first()


# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------

def add_movie(
    db: Session,
    title: str,
    genre: Optional[str] = None,
    rating: Optional[float] = None,
) -> DBMovie:
    """Insert a new movie and return the persisted row."""
    title = title.strip()
    if not title:
        raise ValueError("Movie title cannot be empty.")

    movie = DBMovie(title=title, genre=genre, rating=rating)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------

def update_movie(
    db: Session,
    movie_id: int,
    title: Optional[str] = None,
    genre: Optional[str] = None,
    rating: Optional[float] = None,
) -> DBMovie:
    """Update one or more fields on an existing movie."""
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        raise ValueError(f"Movie with id {movie_id} not found.")

    if title is not None:
        title = title.strip()
        if not title:
            raise ValueError("Movie title cannot be empty.")
        movie.title = title
    if genre is not None:
        movie.genre = genre
    if rating is not None:
        movie.rating = rating

    db.commit()
    db.refresh(movie)
    return movie


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

def delete_movie(db: Session, movie_id: int) -> bool:
    """Delete a movie by id. Returns True on success, raises on not found."""
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        raise ValueError(f"Movie with id {movie_id} not found.")

    db.delete(movie)
    db.commit()
    return True
