from pydantic import BaseModel
from llm_langchain.graph import chat_graph

class ChatPayload(BaseModel):
    chat_id: str
    question: str

def langchain_api(app):
    chat = chat_graph()

    @app.post('/langchain/chat')
    def langchain_chat(payload: ChatPayload):
        config = {'configurable': {'thread_id': payload.chat_id}}
        result = chat.invoke({'messages': payload.question}, config)
        return result['messages'][-1]