from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from typing import Optional

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: int) -> User:
        """ Fetch a user by their ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> User:
        """ Fetch a user by their username."""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> User:
        """ Fetch a user by their email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create_user(self, user: User) -> User:
        """ Create a new user. """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update_user(self, user_id: int, **kwargs) -> User:
        """ Update an existing user. """
        user: User = await self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """ Delete a user by their ID. """
        user: User = await self.get_user_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by their username and password."""
        user = await self.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None
