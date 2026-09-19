from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from .database import get_connection, initialize_database
from .auth import (
    validate_email,
    validate_password,
    hash_password,
    verify_password,
)

app = FastAPI(
    title="Auto Research AI API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database when the API starts
initialize_database()


# =========================
# REQUEST MODELS
# =========================

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def root():
    return {
        "message": "Auto Research AI API is running"
    }


# =========================
# SIGNUP
# =========================

@app.post("/signup")
def signup(user: SignupRequest):

    name = user.name.strip()
    email = str(user.email).lower().strip()
    password = user.password

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name is required."
        )

    if not validate_email(email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email address."
        )

    if not validate_password(password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must contain at least 8 characters, "
                "uppercase, lowercase, number, and special character."
            )
        )

    connection = get_connection()

    existing_user = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists."
        )

    password_hash = hash_password(password)

    connection.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (name, email, password_hash)
    )

    connection.commit()

    user_id = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()["id"]

    connection.close()

    return {
        "message": "Account created successfully.",
        "user_id": user_id,
        "name": name,
        "email": email,
    }


# =========================
# LOGIN
# =========================

@app.post("/login")
def login(user: LoginRequest):

    email = str(user.email).lower().strip()
    password = user.password

    connection = get_connection()

    existing_user = connection.execute(
        """
        SELECT id, name, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        password,
        existing_user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return {
        "message": "Login successful.",
        "user_id": existing_user["id"],
        "name": existing_user["name"],
        "email": existing_user["email"],
    }