import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from pydantic import BaseModel

from backend.database import Database

SECRET_KEY = os.environ.get("SECRET_KEY", "default_unsecure_key")
ALGORITHM = "HS256"


class User(BaseModel):
    email: str = None
    password: str = None


def create_user(user: User) -> None:
    with Database() as connection:
        connection.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)", (user.email, user.password)
        )


def get_user(email: str) -> User:
    with Database() as connection:
        user_row = connection.execute("SELECT * FROM users WHERE email = ?", (email,))
        for row in user_row:
            return User(**row)
        raise Exception("User not found")


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = get_user(username)
    if not user or not password == user.password:
        return False
    return user


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
