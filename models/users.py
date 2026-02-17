from sqlalchemy import Text
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime, timezone
from sqlalchemy import DateTime

from models import Base


class UsersModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False,unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False, default=lambda: datetime.now(timezone.utc))
