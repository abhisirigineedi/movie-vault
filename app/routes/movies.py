<<<<<<< HEAD
"""API routes for the movie wishlist — v1.0 (database-backed)."""

from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
=======
"""API routes for the movie wishlist."""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

>>>>>>> origin/main
from app.services import movie_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


<<<<<<< HEAD
# ---------------------------------------------------------------------------
# Existing endpoints (same URLs — frontend stays unchanged)
# ---------------------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Render the main page with the current movie list."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    # If user is logged in, only fetch their movies. Otherwise fetch none or all? 
    # Let's fetch none if not logged in, since we hide the list anyway.
    movies = movie_service.get_all_movies(db, user_id=user.id) if user else []
    return templates.TemplateResponse(
        "index.html", {"request": request, "movies": movies, "user": user}
=======
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page with the current movie list."""
    movies = movie_service.get_movies()
    return templates.TemplateResponse(
        "index.html", {"request": request, "movies": movies}
>>>>>>> origin/main
    )


@router.post("/add-movie", response_class=HTMLResponse)
<<<<<<< HEAD
async def add_movie(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    genre: str | None = Form(None),
    rating: float | None = Form(None),
):
    """Add a movie and return the updated movie list partial (HTMX)."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    if title.strip():
        try:
            movie_service.add_movie(db, title=title, genre=genre, rating=rating, user=user)
        except ValueError:
            pass  # silently ignore empty-title edge case
    movies = movie_service.get_all_movies(db, user_id=user.id) if user else []
    return templates.TemplateResponse("movie_list.html", {"request": request, "movies": movies, "user": user})


@router.get("/movies", response_class=HTMLResponse)
async def get_movies(request: Request, db: Session = Depends(get_db)):
    """Return the current movie list as an HTML partial."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    movies = movie_service.get_all_movies(db, user_id=user.id) if user else []
    return templates.TemplateResponse("movie_list.html", {"request": request, "movies": movies, "user": user})

@router.delete("/delete-movie/{movie_id}", response_class=HTMLResponse)
async def delete_movie_ui(request: Request, movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie from the UI and return an empty response to remove the element."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    if not user:
        return HTMLResponse(content="Unauthorized", status_code=401)
    try:
        movie_service.delete_movie(db, movie_id, user_id=user.id)
    except (ValueError, PermissionError):
        pass
    return HTMLResponse(content="")


# ---------------------------------------------------------------------------
# New CRUD endpoints (JSON API — for future use / programmatic access)
# ---------------------------------------------------------------------------

@router.get("/api/movies")
async def api_list_movies(request: Request, db: Session = Depends(get_db)):
    """Return the authenticated user's movies as JSON."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    movies = movie_service.get_all_movies(db, user_id=user.id)
    return [
        {"id": m.id, "title": m.title, "genre": m.genre, "rating": m.rating}
        for m in movies
    ]


@router.post("/api/movies")
async def api_add_movie(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Body(...),
    genre: str | None = Body(None),
    rating: float | None = Body(None)
):
    """Add a new movie via JSON for the authenticated user."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        movie = movie_service.add_movie(db, title=title, genre=genre, rating=rating, user=user)
        return {"id": movie.id, "title": movie.title, "genre": movie.genre, "rating": movie.rating}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/movies/{movie_id}")
async def api_get_movie(request: Request, movie_id: int, db: Session = Depends(get_db)):
    """Return a single movie by id, only if owned by the authenticated user."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
        
    movie = movie_service.get_movie_by_id(db, movie_id)
    if movie is None or movie.user_id != user.id:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    return {"id": movie.id, "title": movie.title, "genre": movie.genre, "rating": movie.rating}


@router.put("/api/movies/{movie_id}")
async def api_update_movie(
    request: Request,
    movie_id: int,
    db: Session = Depends(get_db),
    title: str | None = Body(None),
    genre: str | None = Body(None),
    rating: float | None = Body(None),
):
    """Update a movie's fields, only if owned by the authenticated user."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
        
    movie = movie_service.get_movie_by_id(db, movie_id)
    if movie is None or movie.user_id != user.id:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    try:
        movie = movie_service.update_movie(db, movie_id, title=title, genre=genre, rating=rating)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": movie.id, "title": movie.title, "genre": movie.genre, "rating": movie.rating}


@router.delete("/api/movies/{movie_id}")
async def api_delete_movie(request: Request, movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie."""
    from app.services.user_service import get_optional_current_user
    user = await get_optional_current_user(request, db)
    # For API, we might want to check user. If no user, it's public? 
    # v1.1 goal was isolated lists, so API should also require auth for delete.
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
        
    try:
        movie_service.delete_movie(db, movie_id, user_id=user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return {"detail": "Movie deleted"}
=======
async def add_movie(request: Request, title: str = Form(...)):
    """Add a movie and return the updated movie list partial (HTMX)."""
    if title.strip():
        movie_service.add_movie(title)
    movies = movie_service.get_movies()
    # Return only the movie-list partial so HTMX can swap it in-place
    movie_items = "".join(
        f'<li><span class="movie-number">{i}.</span> {m.title}</li>'
        for i, m in enumerate(movies, 1)
    )
    return HTMLResponse(content=movie_items)


@router.get("/movies", response_class=HTMLResponse)
async def get_movies():
    """Return the current movie list as an HTML partial."""
    movies = movie_service.get_movies()
    movie_items = "".join(
        f'<li><span class="movie-number">{i}.</span> {m.title}</li>'
        for i, m in enumerate(movies, 1)
    )
    return HTMLResponse(content=movie_items)
>>>>>>> origin/main
