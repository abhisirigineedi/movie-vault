<<<<<<< HEAD
# 🎬 Movie Vault — v1.3

Movie Vault is a sleek, modern web application for managing your personal movie wishlist. Built with **FastAPI**, **HTMX**, and **SQLAlchemy**, it offers a fast, interactive experience with persistent database storage.

## 🚀 Key Features — v1.3 (Security & Stability)

- **Total Data Privacy**: User wishlists are 100% isolated. No more data leakage between accounts.
- **Strict Data Integrity**: Implemented `AUTOINCREMENT` and `ON DELETE CASCADE` to ensure that when a user is deleted, all their associated movies, ratings, and favorites are also purged.
- **Automatic Auditing**: Every user and movie record now includes a `created_at` timestamp for better data management.
- **Sleek UI/UX**: HTMX-powered interactions for a "single-page" feel without the complexity of a heavy frontend framework.
- **Deployment Ready**: Fully configured for both SQLite (local) and PostgreSQL (production/Render).

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python 3.9+)
- **ORM**: SQLAlchemy 2.0+
- **Database**: SQLite (default), PostgreSQL (supported)
- **Frontend**: HTMX, Jinja2, Vanilla CSS
- **Auth**: JWT (JSON Web Tokens) with Secure Cookies

## 📦 Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/movie-vault.git
    cd movie-vault
    ```

2.  **Set up a virtual environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    source .venv/bin/activate  # macOS/Linux
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    SECRET_KEY=your_super_secret_key_here
    DATABASE_URL=sqlite:///./movies.db
    ```

5.  **Run the application**:
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    Visit `http://127.0.0.1:8000` to start your wishlist!

## 🔐 Data Security & Isolation
In v1.3, we've implemented major security improvements to guarantee user data isolation:
- **ID Reuse Protection**: By using `AUTOINCREMENT`, we ensure that new users never inherit IDs (and thus old data) from deleted accounts.
- **Ownership Enforcement**: Every movie operation (Add, View, Delete) now strictly verifies the owner's `user_id` against the authenticated session.
- **Cascading Purge**: SQLite foreign keys are now strictly enforced via `PRAGMA foreign_keys = ON`, ensuring zero orphaned records.

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

## API Endpoints

| Method   | URL                      | Description                      |
| -------- | ------------------------ | -------------------------------- |
| `GET`    | `/version`               | API version check (v1.1)         |
| `GET`    | `/`                      | Main page (HTML)                 |
| `GET`    | `/login`                 | User Login Page                  |
| `GET`    | `/signup`                | User Registration Page           |
| `GET`    | `/logout`                | Invalidate Session Cookie        |
| `POST`   | `/add-movie`             | Add movie via form (HTMX)        |
| `GET`    | `/movies`                | Movie list partial (HTMX)        |
| `DELETE` | `/delete-movie/{id}`     | Delete movie from UI (HTMX)      |
| `GET`    | `/api/movies`            | List all movies (JSON)           |
| `POST`   | `/api/movies`            | Add a movie (JSON)               |
| `GET`    | `/api/movies/{id}`       | Get one movie (JSON)             |
| `PUT`    | `/api/movies/{id}`       | Update a movie (JSON)            |
| `DELETE` | `/api/movies/{id}`       | Delete a movie (JSON)            |

Interactive docs: **http://localhost:8000/docs**
=======
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
>>>>>>> origin/main

## Project Structure

```
repo-root/
├── app/
<<<<<<< HEAD
│   ├── __init__.py              # Python package marker
│   ├── main.py                  # FastAPI entry point (v1.1)
│   ├── database.py              # SQLAlchemy engine & session setup
│   ├── models/
│   │   ├── db_movie.py          # Movie ORM model
│   │   ├── movie.py             # Pydantic schemas for movies
│   │   └── user.py              # User ORM model & Pydantic schemas
│   ├── services/
│   │   ├── movie_service.py     # CRUD functions for movies & ratings
│   │   └── user_service.py      # CRUD functions for users & authentication
│   ├── routes/
│   │   ├── movies.py            # Movie-related routes (HTML + JSON)
│   │   └── auth.py              # Sign-up, Sign-in, Logout routes
│   └── templates/
│       ├── index.html            # Home page (movie listing)
│       ├── login.html            # Sign-in page
│       ├── signup.html           # Sign-up page
│       └── movie_list.html       # Movie table partial (HTMX)
├── static/
│   ├── styles.css                # Global styling / dark mode
│   └── scripts.js                # Optional JS for stars / interactive ratings
├── .env                          # Environment variables (not committed)
├── .gitignore                    # Ignore .venv, __pycache__, .db, etc.
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render deployment blueprint
├── README.md                     # Project info + instructions
└── movies.db                     # SQLite database (for dev only)
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

=======
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
>>>>>>> origin/main
