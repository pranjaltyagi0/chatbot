from pydantic import BaseModel
from typing import Optional


class SignupSchema(BaseModel):
    fullname: str
    user_email_id: str
    password: str


class LoginSchema(BaseModel):
    user_email_id: str
    password: str


class Token(BaseModel):
    successful: bool
    user_email_id: str | None = None
    access_token: str | None = None
    token_type: str | None = None
