from sqlalchemy import select

from backend.models.recommendations import RecommendationsModel
from backend.schemas.recommendations import RecommedationsAnswerSchema


async def recommendations(db):
    result = await db.execute(select(RecommendationsModel))
    return [RecommedationsAnswerSchema.model_validate(item) for item in result.scalars().all()]