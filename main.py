import dotenv
from fastapi import FastAPI

dotenv.load_dotenv()

app = FastAPI()

@app.get("/")
def index():
    return {"message": "FastAPI For LLM RAG"}

# langchain
from llm_langchain.api import langchain_api
langchain_api(app)

# # llama-index
# from llm_llama_index.api import llama_index_api
# llama_index_api(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)