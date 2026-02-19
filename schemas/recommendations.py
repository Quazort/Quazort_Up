import enum

from pydantic import BaseModel, ConfigDict


class RecommendationType(enum.Enum):
    general = "general"
    training = "training"
    sleep = "sleep"
    nutrition = "nutrition"


class RecommedationsAnswerSchema(BaseModel):
    id: int
    recommendation_type: RecommendationType
    description: str

    model_config = ConfigDict(from_attributes=True)