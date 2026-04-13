from pydantic import BaseModel, ConfigDict


class ExerciseSchema(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class RockResponseSchema(BaseModel):
    muscle_id: int
    muscle_name: str
    muscle_description: str
    exercises: list[ExerciseSchema]

    model_config = ConfigDict(from_attributes=True)

