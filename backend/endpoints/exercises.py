from fastapi import APIRouter
from fastapi.params import Depends

from backend.db.engine import get_session
from backend.services.recommendations import recommendations

exercises_router = APIRouter(tags=["Exercises"])



@exercises_router.get("/general/recommendations")
async def get_recommendations(session = Depends(get_session)):
    answer = await recommendations(session)
    return answer