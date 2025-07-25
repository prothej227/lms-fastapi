from app.services.auth import (
    create_user,
    get_user,
    login_user,
    update_user,
)
from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.user import UserBase, UserLogin
from app.schemas.generic import GenericResponse
from app.database import get_db
from app.views import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, Response

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
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists"
        )
    db_user = await create_user(user_repo, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User creation failed"
        )
    return GenericResponse(
        status_code=status.HTTP_201_CREATED,
        message=f"User {user.username} created successfully",
    )

@auth_router.post("/login", response_model=GenericResponse)
async def authenticate_user(
    response: Response,
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> GenericResponse:
    """
    Authenticate a user.
    
    Args:
        user (UserBase): The user data to authenticate.
        db (AsyncSession): The database session.
    
    Returns:
        User: The authenticated user object.
    """
    user_repo = UserRepository(db)
    access_token: str = await login_user(user_repo, user.username, user.password)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False
    )
    return GenericResponse(
        status_code=status.HTTP_200_OK,
        message=f"User {user.username} logged in successfully",
    )
