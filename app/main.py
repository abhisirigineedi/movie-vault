<<<<<<< HEAD
"""FastAPI application entry point — Movie Wishlist v1.0."""

from contextlib import asynccontextmanager
=======
"""FastAPI application entry point — Movie Wishlist v0.5 (MVP)."""
>>>>>>> origin/main

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

<<<<<<< HEAD
from app.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.movies import router as movies_router
# ---------------------------------------------------------------------------
# Lifespan: create DB tables on startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables (if they don't exist) when the app starts."""
    # Import models so SQLAlchemy registers them with Base.metadata
    from app.models.db_movie import DBMovie  # noqa: F401
    from app.models.user import Favorite, Rating, User  # noqa: F401

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Movie Wishlist", version="1.1", lifespan=lifespan)
=======
from app.routes.movies import router as movies_router

app = FastAPI(title="Movie Wishlist", version="0.5")
>>>>>>> origin/main

# Serve static assets (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routes
app.include_router(movies_router)
<<<<<<< HEAD
app.include_router(auth_router)


@app.get("/version")
def get_version():
    """Return current API version (sanity check for deployment)."""
    return {"version": "1.2"}

# force reload
=======
>>>>>>> origin/main
