from fastapi import APIRouter
from fastapi.params import Depends

from backend.core.auth import get_current_user
from backend.db.engine import get_session

rock_routes = APIRouter(tags=["Rock"])

# @rock_routes.get("/rock/{muscle_id}")
# async def get_rock(muscle_id: int, user_id = Depends(get_current_user), db= Depends(get_session)):
#     # list_of_exercices = rock_muscles(db)
#     return None
