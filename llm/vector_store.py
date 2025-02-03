import os
from llm.model import huggingface_embedding
from llama_index.core import Settings, VectorStoreIndex
from pythainlp.tokenize import word_tokenize
from llama_index.core.node_parser import  TokenTextSplitter
from llama_index.core import SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

def custom_thai_splitter(text):
    return word_tokenize(text, engine="newmm")  # ใช้ Newmm จาก pythainlp

def create_vector_store():
    documents = SimpleDirectoryReader("data/md").load_data()

    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[
            TokenTextSplitter(
                tokenizer=custom_thai_splitter,
                # chunk_size=1000,
            )
        ],
        show_progress=True
    )

    index.storage_context.persist(persist_dir="vector_store")

def load_vector_store():
    storage_context = StorageContext.from_defaults(persist_dir="vector_store")
    index = load_index_from_storage(storage_context)
    return index