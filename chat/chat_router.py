from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection

from chat import ChatController, ChatRequestMessageBody
from utils import get_chat_collection

router = APIRouter()


def get_chat_controller(
    chat_collection: Collection = Depends(get_chat_collection),
) -> ChatController:
    return ChatController(chat_collection)


@router.post("/response")
async def post_llm_response(
    body: ChatRequestMessageBody,
    chat_controller: ChatController = Depends(get_chat_controller),
) -> str:
    try:

        print(body)
        return await chat_controller.content_generator(
            user_email_id=body.user_email_id, body=body
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(
            f"Error occured while generating response from LLM for {body.user_email_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Failed to generate response.")
