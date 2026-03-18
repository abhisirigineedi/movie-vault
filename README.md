# 🎬 Movie Wishlist — v0.5 (MVP)

A simple, clean FastAPI web app to keep track of movies you want to watch.

## Features

- Add movies via a sleek HTMX-powered form (no page reloads)
- In-memory storage (no database required)
- Premium dark-mode UI with animated gradients

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
uvicorn app.main:app --reload
```

Then open **http://localhost:8000** in your browser.

## API Docs

FastAPI auto-generates interactive docs at **http://localhost:8000/docs**.

## Project Structure

```
repo-root/
├── app/
│   ├── __init__.py        ✅ (important — marks app as a Python package)
│   ├── main.py            # FastAPI entry point
│   ├── routes/
│   │   └── movies.py      # API routes (GET /, POST /add-movie, GET /movies)
│   ├── services/
│   │   └── movie_service.py  # In-memory business logic
│   ├── models/
│   │   └── movie.py       # Pydantic model
│   └── templates/
│       └── index.html     # HTMX-powered frontend
├── static/
│   └── styles.css         # Premium dark-mode styling
├── requirements.txt
└── README.md
```

## Tech Stack

| Layer    | Technology    |
| -------- | ------------- |
| Backend  | FastAPI       |
| Frontend | HTMX + Jinja2 |
| Styling  | Vanilla CSS   |
| Server   | Uvicorn       |

## 🚀 Live Demo

🔗 https://movie-vault-zw9w.onrender.com/

> Try adding a movie and see it update instantly ⚡
