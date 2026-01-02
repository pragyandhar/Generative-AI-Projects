# IMPORT
import os
from langchain_openai import ChatOpenAI

def get_proxy_model():
    """
    Return an OpenAI model that uses a custom base URL / proxy URL.
    """
    proxy_url = "http://localhost:8000/v1"
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=proxy_url,   # set base url as proxy url
        temperature=0.5,
    )
