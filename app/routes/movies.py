"""API routes for the movie wishlist."""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services import movie_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page with the current movie list."""
    movies = movie_service.get_movies()
    return templates.TemplateResponse(
        "index.html", {"request": request, "movies": movies}
    )


@router.post("/add-movie", response_class=HTMLResponse)
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
