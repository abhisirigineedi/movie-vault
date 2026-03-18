from pydantic import BaseModel


class Movie(BaseModel):
    """Pydantic model representing a movie in the wishlist."""

    title: str
