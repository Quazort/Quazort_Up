from fastapi import APIRouter
from fastapi.params import Depends

from backend.controllers.users import delete_me
from backend.core.auth import get_current_user
from backend.db.engine import get_session
from backend.schemas.users import DeleteUserSchema

users_routes = APIRouter()


@users_routes.delete("/users/delete")
async def delete_user(password: DeleteUserSchema, db=Depends(get_session), user=Depends(get_current_user)):
    result = await delete_me(db, user, password.password)
    return result
