from sqlalchemy import select, and_

from backend.core.exeptions import RockError
from backend.logger.logger import logger
from backend.models.exercises_muscles import ExercisesMusclesModel, MusclesModel, ExercisesModel
from backend.schemas.rock import RockResponseSchema, ExerciseSchema


async def get_all_muscles_rock(db, muscle_id: int):
    try:
        exercises_query = await db.execute(
            select(
                MusclesModel.id.label("muscle_id"),
                MusclesModel.name.label("muscle_name"),
                MusclesModel.description.label("muscle_description"),
                ExercisesModel.id.label("exercise_id"),
                ExercisesModel.name.label("exercise_name"),
                ExercisesModel.description.label("exercise_description"),
            )
            .select_from(MusclesModel)
            .outerjoin(
                ExercisesMusclesModel,
                (ExercisesMusclesModel.muscle_id == MusclesModel.id) &
                (ExercisesMusclesModel.role == "primary")
            )
            .outerjoin(
                ExercisesModel,
                ExercisesMusclesModel.exercise_id == ExercisesModel.id
            )
            .where(MusclesModel.id == muscle_id)
        )

        exercises_query_response = exercises_query.mappings().all()

        if not exercises_query_response:
            raise RockError()

        rock_preparation_response = RockResponseSchema(
                muscle_id=muscle_id,
                muscle_name=exercises_query_response[0]['muscle_name'],
                muscle_description=exercises_query_response[0]['muscle_description'],
                exercises=[]
            )

        if not exercises_query_response[0]["exercise_id"]:
            return rock_preparation_response

        rock_response = RockResponseSchema(muscle_id=rock_preparation_response.muscle_id,
                                           muscle_name=rock_preparation_response.muscle_name,
                                           muscle_description=rock_preparation_response.muscle_description,
                                           exercises=[ExerciseSchema(id=i['exercise_id'], name=i['exercise_name'],
                                                                     description=i['exercise_description']) for i in
                                                      exercises_query_response])
        return rock_response
    except Exception as e:
        logger.exception(f"get_all_muscles_rock {e}")
        raise
