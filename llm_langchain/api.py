from pydantic import BaseModel
from llm_langchain.graph import chat_graph

class ChatPayload(BaseModel):
    chat_id: str
    question: str

chat = chat_graph()

def langchain_chat(chat_id: str, question: str):
    config = {'configurable': {'thread_id': chat_id}}
    result = chat.invoke({'messages': question}, config)
    return result['messages'][-1].content

def langchain_api(app):
    @app.post('/langchain/chat')
    def langchain_chat(payload: ChatPayload):
        config = {'configurable': {'thread_id': payload.chat_id}}
        result = chat.invoke({'messages': payload.question}, config)
        return result['messages'][-1]