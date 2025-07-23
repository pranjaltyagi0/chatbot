import os
from pymongo.collection import Collection

from .auth_model import SignupRequestBody, LoginRequestBody
from utils import get_user_collection


class AuthController:
    def __init__(self, user_collection: Collection):
        self.user_collection = user_collection

    async def verify_user(self, request: LoginRequestBody):
        try:
            resp = await self.user_collection.find_one(
                {"user_email_id": request.user_email_id, "password": request.password}
            )
            if resp is None:
                return {
                    "message": "Email Id or password is incorrect",
                    "jwt_token": "None",
                }
            else:
                return {"message": "Login successful", "jwt_token": "token"}
        except Exception:
            raise

    async def create_user(self, request: SignupRequestBody):
        try:
            resp = await self.user_collection.find_one(
                {"user_email_id": request.user_email_id}
            )
            if resp is not None:
                return {"message": "Email Id already exists"}

            result = await self.user_collection.insert_one(request.model_dump())
            print(result)
            if result.inserted_id:
                print(result.inserted_id)
                return {"message": "User created Successfully", "jwt_token": "token"}
            else:
                return {"message": "Something went wrong", "jwt_token": "None"}

        except Exception:
            raise
