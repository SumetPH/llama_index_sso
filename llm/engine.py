from llm.vector_store import load_vector_store
from llm.model import google_gemini
from llm.prompt import system_prompt
from llama_index.core.memory import ChatMemoryBuffer

chat_sessions = {}

def chat_engine_context(chat_id: str):
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = ChatMemoryBuffer.from_defaults(
            chat_store_key=chat_id,
            token_limit=10000
        )

    index = load_vector_store()
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=chat_sessions[chat_id],
        llm=google_gemini(),
        system_prompt=system_prompt,
        verbose=True,
    )

    return chat_engine