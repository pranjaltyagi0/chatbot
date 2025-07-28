from typing import Dict

from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection

from auth import LoginSchema, SignupSchema, AuthController, Token
from utils import get_user_collection

router = APIRouter()


async def get_auth_controller(
    user_collection: Collection = Depends(get_user_collection),
) -> AuthController:
    return AuthController(user_collection=user_collection)


@router.post("/login", response_model=Token)
async def login(
    request: LoginSchema,
    auth_controller: AuthController = Depends(get_auth_controller),
) -> Dict[str, str]:
    try:
        response = await auth_controller.verify_user_identity(request)
        print(response)

        return response
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Error occured while loggin in {request.user_email_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong.")


@router.post("/signup", response_model=Token)
async def signup(
    body: SignupSchema,
    auth_controller: AuthController = Depends(get_auth_controller),
) -> Dict[str, str]:
    try:
        response = await auth_controller.register_new_user(body)
        return response
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(
            f"Error occured while generating response from LLM for {body.user_email_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Something went wrong.")
