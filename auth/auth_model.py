from pydantic import BaseModel
from typing import Optional


class SignupRequestBody(BaseModel):
    first_name: str
    last_name: Optional[str]
    user_email_id: str
    password: str


class LoginRequestBody(BaseModel):
    user_email_id: str
    password: str


class ResponseModel(BaseModel):
    message: str
    jwt_token: str | None
