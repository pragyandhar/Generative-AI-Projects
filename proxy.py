import os
from langchain_openai import ChatOpenAI

def proxy_model(base_url: str):
    return ChatOpenAI(
        api_key = os.getenv("OPENAI_API_KEY"),
        base_url=base_url,
    )