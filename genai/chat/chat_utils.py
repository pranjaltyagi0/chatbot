from typing import List, Any, Union, Dict
from langchain_groq import ChatGroq

from prompt_manager import prompt_engine


async def standalone_question(
    question: str, chat_history: List[Dict[str, str]], llm: ChatGroq
) -> str:
    prompt = await prompt_engine.get_prompt(
        "chatbot_prompt",
        "standalone_question",
        chat_history=chat_history,
        question=question,
    )
    print(prompt)
    new_question = await llm.ainvoke(prompt)
    return new_question.content


def format_chat_history(
    chat_history: List[Dict[str, str | None]],
) -> List[Dict[str, str]]:
    try:
        transformed = []
        for entry in chat_history:
            transformed.append({"role": "user", "content": entry["user"]})
            transformed.append(
                {
                    "role": "assistant",
                    "content": entry.get("assistant", "No response available")
                    or "No response available",
                }
            )
        return transformed
    except KeyError:
        raise ValueError(f"Key missing in chat history")
