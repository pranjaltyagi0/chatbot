import os
import json
import httpx
from fastapi import Request, Response

from chat import ChatRequestMessageBody
from utils import get_chat_history_collection


class ChatController:
    def __init__(self, chat_collection):
        self.internal_server = os.getenv("INTERNAL_SERVER")
        self.chat_collection = chat_collection

    async def llm_response(self, body: ChatRequestMessageBody, request: Request):
        chat_doc = await get_chat_history_collection().find_one(
            {"user_email_id": body.user_email_id}
        )
        payload = {
            "user_email_id": body.user_email_id,
            "chat_history": chat_doc["chat_history"] if chat_doc else [],
            "question": body.question,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self.internal_server}/chat/response", json=payload
            )
            print(response.text)
            print(response.status_code)

        await self.chat_history(body, response)
        # response = json.loads(response)
        return response.text

    async def chat_history(self, body: ChatRequestMessageBody, response: Response):
        chat_doc = await get_chat_history_collection().find_one(
            {"user_email_id": body.user_email_id}
        )

        if chat_doc is None:
            # Create new chat history document
            await get_chat_history_collection().insert_one(
                {
                    "user_email_id": body.user_email_id,
                    "chat_history": [
                        {"user": body.question, "assistant": response.text}
                    ],
                }
            )
        else:
            # Append new message to chat history
            await get_chat_history_collection().update_one(
                {"user_email_id": body.user_email_id},
                {
                    "$push": {
                        "chat_history": {
                            "user": body.question,
                            "assistant": response.text,
                        }
                    }
                },
            )
