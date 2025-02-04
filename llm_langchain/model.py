from langchain_google_genai import ChatGoogleGenerativeAI

def google_gemini():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
    )