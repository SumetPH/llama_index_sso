import os
from langchain_unstructured import UnstructuredLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from pythainlp.tokenize import word_tokenize

vector_store_path = "llm_langchain/vector_db"
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

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