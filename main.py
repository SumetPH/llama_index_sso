import dotenv
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from llm.engine import chat_engine_context
from llm.model import huggingface_embedding
from llama_index.core import set_global_handler, Settings
from llama_index.core.memory import ChatMemoryBuffer

dotenv.load_dotenv()

Settings.embed_model = huggingface_embedding()
# logging.basicConfig(level=logging.DEBUG)
# set_global_handler("simple")

app = FastAPI()

class ChatPayload(BaseModel):
    id: str
    question: str

@app.get("/")
def index():
    return {"message": "FastAPI For ChatBot"}

@app.post('/chat')
def chat(payload: ChatPayload):
    engine = chat_engine_context(chat_id=payload.id)
    output = engine.chat(payload.question)
    return {"message": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)