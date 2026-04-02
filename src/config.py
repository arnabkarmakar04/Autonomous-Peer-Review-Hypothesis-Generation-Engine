import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
# from langchain_groq import ChatGroq

def get_llm(temperature=0):
    """Instantiates the LLM. Swap this to ChatGroq if preferred."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=temperature,
        max_retries=2
    )
    
    # return ChatGroq(
    #     model="llama-3.1-8b-instant", 
    #     temperature=temperature
    # )