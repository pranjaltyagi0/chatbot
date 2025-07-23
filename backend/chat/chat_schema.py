from pydantic import BaseModel
from typing import Optional, List, Any


class ChatRequestMessageBody(BaseModel):
    user_email_id: str
    question: str

