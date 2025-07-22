from fastapi import FastAPI, APIRouter

from .auth_controller import AuthController
from .auth_model import SignUp, Login

router = APIRouter()


@router.post("/login")
async def login(request: Login):
    result = await AuthController().login(request=request)
    # print(db)
    return result


@router.post("/signup")
async def signup(request: SignUp):
    response = await AuthController().signup(request=request)
    return response
