from fastapi import APIRouter
from fastapi.params import Depends

from backend.controllers.rock import rock_muscles
from backend.core.auth import oauth2_scheme, get_current_user
from backend.db.engine import get_session

rock_routes = APIRouter(tags=["Rock"])

@rock_routes.get("/rock/{muscle_id}")
async def get_rock(muscle_id: int,user = Depends(get_current_user), db= Depends(get_session)):
    list_of_exercices = await rock_muscles(db, muscle_id)
    return list_of_exercices
