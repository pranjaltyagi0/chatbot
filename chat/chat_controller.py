import os
import json
import httpx
from fastapi import Request

from chat import ChatRequestMessageBody


class ChatController:
    def __init__(self, chat_collection):
        self.internal_server = os.getenv("INTERNAL_SERVER")
        self.chat_collection = chat_collection

    async def llm_response(self, body: ChatRequestMessageBody, request: Request):
        payload = {
            "user_email_id": body.user_email_id,
            "chat_history": body.chat_history,
            "question": body.question,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self.internal_server}/chat/response", json=payload
            )
            print(response.text)
            # response = json.loads(response)
        return response.text
