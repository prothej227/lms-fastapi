from sqlalchemy import Column, Integer, String, Boolean,DateTime
from app.database import Base
from passlib.context import CryptContext
from datetime import datetime, timezone
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, str(self.password_hash))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
        }
