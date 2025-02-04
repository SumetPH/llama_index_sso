import os
from pythainlp.tokenize import word_tokenize
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import  TokenTextSplitter
from llama_index.core import SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage

vector_store_path = "llm_llama_index/vector_db"

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

    index.storage_context.persist(persist_dir=vector_store_path)
    return index

def load_vector_store():
    if os.path.exists(vector_store_path):
        storage_context = StorageContext.from_defaults(persist_dir=vector_store_path)
        index = load_index_from_storage(storage_context)
        return index
    else :
        index = create_vector_store()
        return index
