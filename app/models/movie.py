"""Pydantic schemas for movie data validation and serialisation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Movie(BaseModel):
    """Original schema — kept for backward compatibility."""

    title: str


class MovieCreate(BaseModel):
    """Schema for creating a new movie."""

    title: str = Field(..., min_length=1, max_length=255)
    genre: Optional[str] = Field(None, max_length=100)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)


class MovieUpdate(BaseModel):
    """Schema for updating an existing movie (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    genre: Optional[str] = Field(None, max_length=100)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)


class MovieResponse(BaseModel):
    """Schema for movie responses — includes DB-generated fields."""

    id: int
    title: str
    genre: Optional[str] = None
    rating: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
