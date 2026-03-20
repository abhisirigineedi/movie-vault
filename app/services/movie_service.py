<<<<<<< HEAD
"""Business logic for movie wishlist — SQL database-backed (v1.0)."""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.db_movie import DBMovie


# ---------------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------------

def get_all_movies(db: Session, user_id: Optional[int] = None) -> list[DBMovie]:
    """Return movies for a given user, or all if no user specified."""
    query = db.query(DBMovie)
    if user_id is not None:
        query = query.filter(DBMovie.user_id == user_id)
    return query.order_by(DBMovie.id.asc()).all()


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
    user = None,
) -> DBMovie:
    """Insert a new movie and return the persisted row."""
    from app.models.user import Rating
    title = title.strip()
    if not title:
        raise ValueError("Movie title cannot be empty.")

    movie = DBMovie(title=title, genre=genre, rating=rating, user_id=user.id if user else None)
    db.add(movie)
    db.flush()
    if user and rating:
        new_rating = Rating(user_id=user.id, movie_id=movie.id, rating=rating)
        db.add(new_rating)
        
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

def delete_movie(db: Session, movie_id: int, user_id: Optional[int] = None) -> bool:
    """Delete a movie by id, optionally verifying ownership. Returns True on success."""
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        raise ValueError(f"Movie with id {movie_id} not found.")

    if user_id is not None and movie.user_id != user_id:
        raise PermissionError("You do not have permission to delete this movie.")

    from app.models.user import Rating, Favorite
    db.query(Rating).filter(Rating.movie_id == movie_id).delete()
    db.query(Favorite).filter(Favorite.movie_id == movie_id).delete()

    db.delete(movie)
    db.commit()
    return True
=======
"""Business logic for movie wishlist — in-memory storage (no database)."""

from app.models.movie import Movie

# ---------------------------------------------------------------------------
# Global in-memory movie list
# ---------------------------------------------------------------------------
movies: list[Movie] = []


def add_movie(title: str) -> Movie:
    """Create a Movie and append it to the in-memory list."""
    movie = Movie(title=title.strip())
    movies.append(movie)
    return movie


def get_movies() -> list[Movie]:
    """Return the current list of movies."""
    return movies
>>>>>>> origin/main
