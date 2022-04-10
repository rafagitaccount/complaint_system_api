from fastapi import APIRouter, status

from managers.user import Usermanager
from schemas.request.user import UserLoginIn, UserRegisterIn


router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegisterIn):
    token = await Usermanager.register(user_data.dict())
    return {"token": token}


@router.post("/login/")
async def login(user_data: UserLoginIn):
    token = await Usermanager.login(user_data.dict())
    return {"token": token}
