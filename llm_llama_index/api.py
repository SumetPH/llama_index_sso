from pydantic import BaseModel
from llm_llama_index.engine import chat_engine_context

class ChatPayload(BaseModel):
    chat_id: str
    question: str

def llama_index_api(app):

    @app.post('/llama-index/chat')
    def llama_index_chat(payload: ChatPayload):
        engine = chat_engine_context(chat_id=payload.chat_id)
        result = engine.chat(payload.question)
        return result