import enum

from sqlalchemy import Enum
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime, timezone
from sqlalchemy import DateTime

from backend.models import Base

class User_Type(enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hashed: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                 default=lambda: datetime.now(timezone.utc))
    role: Mapped[User_Type] = mapped_column(Enum(User_Type,name="user_type"),default=User_Type.USER.value,nullable=False)
    deleted: Mapped[bool] = mapped_column(default=False,nullable=False)