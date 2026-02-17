from datetime import datetime, timezone, timedelta

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class RefreshTokenModel(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    token_hash: Mapped[str] = mapped_column(nullable=False)
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,  default=lambda:datetime.now(timezone.utc)+ timedelta(days=7))
    revoked: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda:datetime.now(timezone.utc))
