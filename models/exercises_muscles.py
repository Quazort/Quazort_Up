from sqlalchemy import ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class MusclesModel(Base):
    __tablename__ = 'muscles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    exercise_links: Mapped[list["ExercisesMusclesModel"]] = relationship(
        back_populates="muscle"
    )


class ExercisesModel(Base):
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text)

    muscle_links: Mapped[list["ExercisesMusclesModel"]] = relationship(
        back_populates="exercise"
    )


class ExercisesMusclesModel(Base):
    __tablename__ = 'exercises_muscles'

    muscle_id: Mapped[int] = mapped_column(ForeignKey('muscles.id'), primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'), primary_key=True)
    role: Mapped[str] = mapped_column(Enum(
        'primary',
        'secondary',
        'stabilizer',
        name='muscle_role'
    ),nullable = False, default='secondary')

    muscle: Mapped["MusclesModel"] = relationship(
        back_populates="exercise_links"
    )
    exercise: Mapped["ExercisesModel"] = relationship(
        back_populates="muscle_links"
    )