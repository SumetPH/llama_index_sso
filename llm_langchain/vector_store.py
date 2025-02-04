import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from pythainlp.tokenize import word_tokenize
from llm_langchain.model import huggingface_embedding

vector_store_path = "llm_langchain/vector_db"
embeddings = huggingface_embedding()

def custom_tokenizer(text):
    return "".join(word_tokenize(text, engine="newmm"))

def create_vector_store():
    file_paths = [
        'data/md/chula.md',
        'data/md/finnomena.md',
        'data/md/sso.md',
    ]

    docs = []

    for file_path in file_paths:
        loader = UnstructuredMarkdownLoader(
            file_path,
            mode="elements",
            strategy="fast",
        )
        doc = loader.load()
        docs += doc

    index = FAISS.from_documents(
        docs,
        embeddings, 
    )

    index.save_local(vector_store_path)
    return index

def load_vector_store():
    if os.path.exists(vector_store_path):
        index = FAISS.load_local(
            vector_store_path, 
            embeddings, 
            allow_dangerous_deserialization=True,
        )
        return index
    else:
        index = create_vector_store()
        return index