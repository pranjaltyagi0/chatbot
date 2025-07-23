from pymongo.collection import Collection
from chat import standalone_question, format_chat_history, ChatRequestMessageBody
from utils import LLMManager


class ChatController:
    def __init__(self, chat_collection: Collection):
        self.chat_collection = chat_collection

    async def content_generator(
        self, user_email_id: str, body: ChatRequestMessageBody
    ) -> str:
        try:
            llm_chat = await LLMManager().get_llm()
            formatted_chat_history = format_chat_history(chat_history=body.chat_history)
            new_question = await standalone_question(
                question=body.question.strip(),
                chat_history=formatted_chat_history,
                llm=llm_chat,
            )
            print(new_question)
            response = await llm_chat.ainvoke(new_question)
            return response.content
        except Exception:
            raise
