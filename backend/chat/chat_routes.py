from fastapi import APIRouter, Depends, Request
from pymongo.collection import Collection

from chat import ChatRequestMessageBody, ChatController
from utils import get_chat_collection

router = APIRouter()


async def get_chat_controller(
    chat_collection: Collection = Depends(get_chat_collection),
) -> ChatController:
    return ChatController(chat_collection=chat_collection)


@router.post("/response")
async def request_llm_response(
    request: Request,
    body: ChatRequestMessageBody,
    chat_controller: ChatController = Depends(get_chat_controller),
) -> str:
    return await chat_controller.llm_response(body,request)
