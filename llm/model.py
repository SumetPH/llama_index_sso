from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini

def huggingface_embedding():
    return HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-large")

def google_gemini():
    return Gemini(
        model="models/gemini-1.5-flash",
        temperature=0, 
    )