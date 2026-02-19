from fastapi import APIRouter
from fastapi.params import Depends

from db.engine import get_session
from services.recommendations import recommendations

exercises_router = APIRouter()



@exercises_router.get("/general/recommendations")
async def get_recommendations(session = Depends(get_session)):
    answer = await recommendations(session)
    return answer


