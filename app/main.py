"""FastAPI application entry point — Movie Wishlist v1.0."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes.movies import router as movies_router


# ---------------------------------------------------------------------------
# Lifespan: create DB tables on startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables (if they don't exist) when the app starts."""
    # Import the model so SQLAlchemy registers it with Base.metadata
    from app.models.db_movie import DBMovie  # noqa: F401

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Movie Wishlist", version="1.0", lifespan=lifespan)

# Serve static assets (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routes
app.include_router(movies_router)


@app.get("/version")
def get_version():
    """Return current API version (sanity check for deployment)."""
    return {"version": "v1.0"}
