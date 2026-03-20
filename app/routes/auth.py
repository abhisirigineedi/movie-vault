"""Authentication routes spanning login and signup."""

from datetime import timedelta

from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.user_service import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_user,
    get_optional_current_user,
    get_user_by_username,
    verify_password,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, db: Session = Depends(get_db)):
    """Render the sign-up page."""
    user = await get_optional_current_user(request, db)
    if user:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handle sign-up form submission."""
    # Check if username exists
    if get_user_by_username(db, username):
        return templates.TemplateResponse(
            "signup.html", {"request": request, "error": "Username already exists"}
        )

    # Need get_password_hash from user_service.py
    from app.services.user_service import get_password_hash
    hashed_pw = get_password_hash(password)
    create_user(db, username=username, hashed_password=hashed_pw)

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    """Render the log-in page."""
    user = await get_optional_current_user(request, db)
    if user:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    response: Response,
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handle log-in form submission."""
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    resp = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    resp.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
    )
    return resp


@router.get("/logout")
async def logout():
    """Log out the user by clearing the cookie."""
    resp = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    resp.delete_cookie(key="access_token")
    return resp
