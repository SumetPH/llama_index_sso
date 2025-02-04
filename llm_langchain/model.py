from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

def huggingface_embedding():
    return HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

def google_gemini():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
    )