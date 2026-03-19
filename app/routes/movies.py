"""API routes for the movie wishlist — v1.0 (database-backed)."""

from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import movie_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ---------------------------------------------------------------------------
# Existing endpoints (same URLs — frontend stays unchanged)
# ---------------------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    from app.auth import get_optional_current_user
    user = await get_optional_current_user(request, db)
    movies = movie_service.get_all_movies(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "movies": movies, "user": user}
    )


@router.post("/add-movie", response_class=HTMLResponse)
async def add_movie(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    genre: str | None = Form(None),
    rating: float | None = Form(None),
):
    """Add a movie and return the updated movie list partial (HTMX)."""
    from app.auth import get_current_user, get_optional_current_user
    # Optional logic: could restrict to logged in users, or just handle optional
    user = await get_optional_current_user(request, db)
    if not user:
        return HTMLResponse(content="<p>Please login to add a movie</p>", status_code=401)
        
    if title.strip():
        try:
            movie_service.add_movie(db, title=title, genre=genre, rating=rating, user=user)
        except ValueError:
            pass  # silently ignore empty-title edge case
    movies = movie_service.get_all_movies(db)
    return templates.TemplateResponse("movie_list.html", {"request": request, "movies": movies, "user": user})


@router.get("/movies", response_class=HTMLResponse)
async def get_movies(request: Request, db: Session = Depends(get_db)):
    """Return the current movie list as an HTML partial."""
    movies = movie_service.get_all_movies(db)
    return templates.TemplateResponse("movie_list.html", {"request": request, "movies": movies})

@router.delete("/delete-movie/{movie_id}", response_class=HTMLResponse)
async def delete_movie_ui(movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie from the UI and return an empty response to remove the element."""
    try:
        movie_service.delete_movie(db, movie_id)
    except ValueError:
        pass
    return HTMLResponse(content="")


# ---------------------------------------------------------------------------
# New CRUD endpoints (JSON API — for future use / programmatic access)
# ---------------------------------------------------------------------------

@router.get("/api/movies")
async def api_list_movies(db: Session = Depends(get_db)):
    """Return all movies as JSON."""
    movies = movie_service.get_all_movies(db)
    return [
        {"id": m.id, "title": m.title, "genre": m.genre, "rating": m.rating}
        for m in movies
    ]


@router.post("/api/movies")
async def api_add_movie(
    db: Session = Depends(get_db),
    title: str = Body(...),
    genre: str | None = Body(None),
    rating: float | None = Body(None)
):
    """Add a new movie via JSON."""
    try:
        movie = movie_service.add_movie(db, title=title, genre=genre, rating=rating)
        return {"id": movie.id, "title": movie.title, "genre": movie.genre, "rating": movie.rating}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/movies/{movie_id}")
async def api_get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Return a single movie by id."""
    movie = movie_service.get_movie_by_id(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"id": movie.id, "title": movie.title, "genre": movie.genre, "rating": movie.rating}


@router.put("/api/movies/{movie_id}")
async def api_update_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    title: str | None = Body(None),
    genre: str | None = Body(None),
    rating: float | None = Body(None),
):
    """Update a movie's fields."""
    try:
        movie = movie_service.update_movie(db, movie_id, title=title, genre=genre, rating=rating)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"id": movie.id, "title": movie.title, "genre": movie.genre, "rating": movie.rating}


@router.delete("/api/movies/{movie_id}")
async def api_delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie."""
    try:
        movie_service.delete_movie(db, movie_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"detail": "Movie deleted"}
