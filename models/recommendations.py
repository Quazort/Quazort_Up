from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class RecommendationsModel(Base):
    __tablename__ = 'recommendations'

    id: Mapped[int] = mapped_column(primary_key=True)
    recommendation_type: Mapped[str] = mapped_column(Enum('general','nutrition','training','sleep'),nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
