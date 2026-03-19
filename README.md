# 🎬 Movie Wishlist — v1.0 (SQL + Deployment Ready)

A FastAPI web app to keep track of movies you want to watch — now backed by a real SQL database with full CRUD support and ready for deployment on Render.

## What's New in v1.0

- **SQL database** — movies persist across restarts (SQLite locally, PostgreSQL on Render)
- **Full CRUD** — add, view, update, and delete movies via API
- **Expanded data model** — `genre` and `rating` fields (optional, for future UI)
- **Deployment-ready** — `render.yaml` blueprint for one-click Render deployment
- **Error handling** — input validation, not-found checks, data integrity

## Quick Start (Local)

```bash
# 1. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Copy environment template
copy .env.example .env

# 4. Run the app
uvicorn app.main:app --reload
```

Open **http://localhost:8000** — a `movies.db` SQLite file will be created automatically.

## API Endpoints

| Method   | URL                      | Description                      |
| -------- | ------------------------ | -------------------------------- |
| `GET`    | `/version`               | API version check (v1.0)         |
| `GET`    | `/`                      | Main page (HTML)                 |
| `POST`   | `/add-movie`             | Add movie via form (HTMX)        |
| `GET`    | `/movies`                | Movie list partial (HTMX)        |
| `DELETE` | `/delete-movie/{id}`     | Delete movie from UI (HTMX)      |
| `GET`    | `/api/movies`            | List all movies (JSON)           |
| `POST`   | `/api/movies`            | Add a movie (JSON)               |
| `GET`    | `/api/movies/{id}`       | Get one movie (JSON)             |
| `PUT`    | `/api/movies/{id}`       | Update a movie (JSON)            |
| `DELETE` | `/api/movies/{id}`       | Delete a movie (JSON)            |

Interactive docs: **http://localhost:8000/docs**

## Project Structure

```
repo-root/
├── app/
│   ├── __init__.py            # Python package marker
│   ├── main.py                # FastAPI entry point (v1.0)
│   ├── database.py            # SQLAlchemy engine & session setup
│   ├── routes/
│   │   └── movies.py          # All API routes (HTML + JSON)
│   ├── services/
│   │   └── movie_service.py   # DB-backed CRUD functions
│   ├── models/
│   │   ├── movie.py           # Pydantic schemas
│   │   └── db_movie.py        # SQLAlchemy ORM model
│   └── templates/
│       └── index.html         # HTMX-powered frontend
├── static/
│   └── styles.css             # Premium dark-mode styling
├── requirements.txt
├── render.yaml                # Render deployment blueprint
├── .env.example               # Environment variable template
└── README.md
```

## Deploy to Render

1. Push your code to a GitHub repository.
2. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect your repo — Render will detect `render.yaml` automatically.
4. Click **Apply** — it will create:
   - A free PostgreSQL database (`movie-wishlist-db`)
   - A free web service (`movie-wishlist`) with `DATABASE_URL` auto-configured
5. Wait for the build to finish → your app is live! 🚀

> **Note:** Free-tier services spin down after inactivity. The first request after sleep takes ~30s to cold-start.

## Adding Future Features

To add a new feature safely:

1. **Model** — Add columns to `app/models/db_movie.py` (or create a new model file).
2. **Schema** — Add corresponding Pydantic fields in `app/models/movie.py`.
3. **Service** — Write a new function in `app/services/movie_service.py` (or a new service file).
4. **Route** — Add an endpoint in `app/routes/movies.py` that calls your service function.
5. **Test** — Hit the new endpoint via `/docs` or the frontend.

This function-based pattern ensures new features never break existing ones.

## Tech Stack

| Layer      | Technology           |
| ---------- | -------------------- |
| Backend    | FastAPI              |
| Database   | SQLAlchemy + SQLite / PostgreSQL |
| Frontend   | HTMX + Jinja2        |
| Styling    | Vanilla CSS          |
| Server     | Uvicorn              |
| Deployment | Render               |

## 🚀 Live Demo (v1.0)

🔗 https://movie-vault-zw9w.onrender.com/

🎬 Features:

➕ Add movies dynamically

❌ Delete movies instantly

🔄 Real-time updates

⚡ Fast API-based backend

💡 Try adding and deleting a movie to see instant changes!

⚠️ Note: The app may take 30–60 seconds to load initially (free hosting cold start).

