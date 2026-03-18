"""FastAPI application entry point — Movie Wishlist v0.5 (MVP)."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.movies import router as movies_router

app = FastAPI(title="Movie Wishlist", version="0.5")

# Serve static assets (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routes
app.include_router(movies_router)
