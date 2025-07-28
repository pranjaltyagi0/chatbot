import os
import jwt
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from pymongo.collection import Collection

from utils import get_user_collection

from .auth_model import LoginSchema, SignupSchema, Token


class AuthController:
    def __init__(self, user_collection: Collection):
        self.user_collection = user_collection
        self.jwt_secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    def create_hashed_password(self, plaintext_password):
        pwd_context = CryptContext(schemes=["bcrypt"])
        return pwd_context.hash(plaintext_password)

    def verify_password(self, plaintext_password, hashed_password):
        pwd_context = CryptContext(schemes=["bcrypt"])
        return pwd_context.verify(plaintext_password, hashed_password)

    def create_jwt_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.jwt_secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    async def verify_user_identity(self, request: LoginSchema):
        try:
            user_email_id, password = (
                request.user_email_id,
                request.password,
            )
            response = await self.user_collection.find_one(
                {"user_email_id": user_email_id}
            )
            if response is None:
                return {"successful": False, "message": "Account does not exist"}
            isPasword = self.verify_password(
                plaintext_password=password, hashed_password=response["password"]
            )
            if isPasword:
                access_token_expires = timedelta(
                    minutes=self.access_token_expire_minutes
                )
                jwt_token = self.create_jwt_token(
                    data={"sub": request.user_email_id},
                    expires_delta=access_token_expires,
                )
                return Token(
                    successful=True,
                    user_email_id=user_email_id,
                    access_token=jwt_token,
                    token_type="bearer",
                )
            return Token(successful=False)
        except Exception:
            raise

    async def register_new_user(self, request: SignupSchema):
        try:
            fullname, user_email_id, password = (
                request.fullname,
                request.user_email_id,
                request.password,
            )
            response = await self.user_collection.find_one(
                {"user_email_id": user_email_id}
            )
            if response is not None:
                return {"message": "Email id already exists"}

            hashed_password = self.create_hashed_password(plaintext_password=password)
            print(hashed_password)
            result = await self.user_collection.insert_one(
                {
                    "fullname": fullname,
                    "user_email_id": user_email_id,
                    "password": hashed_password,
                }
            )
            print(result)
            if result.inserted_id:
                access_token_expires = timedelta(
                    minutes=self.access_token_expire_minutes
                )
                jwt_token = self.create_jwt_token(
                    data={"sub": request.user_email_id},
                    expires_delta=access_token_expires,
                )
                return Token(
                    successful=True,
                    user_email_id=user_email_id,
                    access_token=jwt_token,
                    token_type="bearer",
                )
            return Token(successful=False)

        except Exception:
            raise
