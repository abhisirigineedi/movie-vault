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
