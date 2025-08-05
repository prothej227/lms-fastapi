from app.services.auth import (
    create_user,
    get_user,
    login_user,
    update_user,
)
from app.repositories.user import UserRepository
from app.schemas.user import UserBase, UserLogin, UserView
from app.schemas.generic import GenericResponse, LoginResponse
from app.database import get_db
from app.views import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, Response, Request
from jose import jwt, JWTError
from app.core.config import get_settings
from app.core import messages

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=GenericResponse)
async def register_user(
    user: UserBase,
    db: AsyncSession = Depends(get_db),
) -> GenericResponse:
    """
    Register a new user.

    Args:
        user (UserBase): The user data to create.
        db (AsyncSession): The database session.

    Returns:
        User: The created user object.
    """
    user_repo = UserRepository(db)
    existing_user = await user_repo.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    db_user = await create_user(user_repo, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed"
        )
    return GenericResponse(
        status_code=status.HTTP_201_CREATED,
        message=f"User {user.username} created successfully",
    )


@auth_router.post("/login", response_model=LoginResponse)
async def authenticate_user(
    response: Response,
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> LoginResponse:
    """
    Authenticate a user.

    Args:
        user (UserBase): The user data to authenticate.
        db (AsyncSession): The database session.

    Returns:
        User: The authenticated user object.
    """
    user_repo = UserRepository(db)
    login_result = await login_user(user_repo, user.username, user.password)
    if not login_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    user_data = login_result.get("user", dict())
    access_token = login_result.get("access_token", "")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False,
    )
    return LoginResponse(
        message=f"User {user_data.username} authenticated successfully",
        access_token=access_token,
        user=UserView(
            id=user_data.id,
            email=user_data.email,
            username=user_data.username,
            role=user_data.role,
            is_active=user_data.is_active,
            full_name=(
                f"{user_data.first_name} {user_data.last_name}"
                if user_data.first_name and user_data.last_name
                else None
            ),
        ),
    )


@auth_router.get("/me", response_model=LoginResponse)
async def get_me(request: Request):
    """
    Get the currently authenticated user.

    Returns:
        User: The authenticated user object.
    """
    # This function would typically extract the user from the request context
    # or session, but for simplicity, we return a placeholder here.
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
    return LoginResponse(
        message="User session is still active.",
        access_token=token,
        user=UserView(
            id=payload.get("id"),
            email=payload.get("email"),
            username=payload.get("sub"),
            role=payload.get("role"),
            is_active=payload.get("is_active"),
            full_name=payload.get("full_name"),
        ),
    )
