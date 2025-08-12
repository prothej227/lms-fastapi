from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.user import UserBase
from typing import Optional, Dict
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import get_settings
from typing import Optional, Any
from fastapi import Request, HTTPException, status
from app.schemas.user import UserView
from app.core import messages
from zoneinfo import ZoneInfo


def create_access_token(data: Dict, expires_delta: int = 0) -> str:
    """Create an access token for the user."""
    to_encode = data.copy()
    expire = (
        datetime.now(ZoneInfo(get_settings().timezone))
        + timedelta(minutes=expires_delta)
        if expires_delta
        else None
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, get_settings().secret_key, algorithm=get_settings().algorithm
    )
    return encoded_jwt


def verify_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, get_settings().secret_key, algorithms=[get_settings().algorithm]
        )
        username: str = payload.get("sub") or ""
        if username is None:
            return None
        return username
    except JWTError:
        return None


async def create_user(db: UserRepository, user: UserBase) -> Optional[User]:
    """
    Create a new user in the database.

    Args:
        db (UserRepository): The database session.
        user (UserBase): The user data to create.

    Returns:
        User: The created user object.
    """

    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
    )
    db_user.set_password(user.password)
    await db.create_user(db_user)
    return db_user


async def get_user(db: UserRepository, user_id: int) -> User:
    """
    Get a user by their ID.

    Args:
        db (UserRepository): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """
    return await db.get_user_by_id(user_id)


async def update_user(db: UserRepository, user_id: int, **kwargs) -> User:
    """
    Update an existing user.

    Args:
        db (UserRepository): The database session.
        user_id (int): The ID of the user to update.
        **kwargs: The fields to update.

    Returns:
        User: The updated user object if successful, None otherwise.
    """
    return await db.update_user(user_id, **kwargs)


async def delete_user(db: UserRepository, user_id: int) -> bool:
    """
    Delete a user by their ID.

    Args:
        db (UserRepository): The database session.
        user_id (int): The ID of the user to delete.

    Returns:
        bool: True if the user was deleted, False otherwise.
    """
    return await db.delete_user(user_id)


async def get_user_by_username(db: UserRepository, username: str) -> User:
    """
    Get a user by their username.

    Args:
        db (UserRepository): The database session.
        username (str): The username of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """
    return await db.get_user_by_username(username)


async def login_user(
    db: UserRepository, username: str, password: str
) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user by their username and password.

    Args:
        db (UserRepository): The database session.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User: The authenticated user object if successful, None otherwise.
    """
    user = await db.authenticate_user(username, password)
    if not user:
        return None
    access_token = create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "full_name": (
                f"{user.first_name} {user.last_name}"
                if bool(user.first_name) and bool(user.last_name)
                else None
            ),
        },
        expires_delta=60,
    )
    return {
        "user": user,
        "access_token": access_token,
    }


async def get_current_user(request: Request) -> UserView:
    """
    Get current user or session instance

    Args:
        request: The HTTP payload request
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.AUTH_NO_ACTIVE_SESSION,
        )
    try:
        payload = jwt.decode(
            token=token,
            key=get_settings().secret_key,
            algorithms=[get_settings().algorithm],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.AUTH_INVALID_TOKEN
        )
    _payload_username = payload.get("sub")
    _payload_id = payload.get("id")
    return UserView(
        id=_payload_id if _payload_id else -1,
        email=payload.get("email"),
        username=_payload_username if _payload_username else "",
        role=payload.get("role"),
        is_active=payload.get("is_active"),
        full_name=payload.get("full_name"),
    )
