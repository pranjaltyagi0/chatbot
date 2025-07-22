import os
from langchain_groq import ChatGroq


class LLMManager:
    _instance = None
    _llm_instance: ChatGroq = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.load_config()

    def load_config(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL")

    async def get_llm(self):
        if LLMManager._llm_instance is None:
            LLMManager._llm_instance = ChatGroq(
                model=self.model,
                temperature=0.7,
                api_key=self.groq_api_key,
                streaming=True,
            )
        return LLMManager._llm_instance
