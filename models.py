import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def _get_model():
    """Lazy initialization of model"""
    return ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True
    )

def invoke_model(prompt: str):
    model = _get_model()
    msg = [HumanMessage(content=prompt)]
    resp = model.invoke(msg)
    return {"text": resp.text}

def stream_model(prompt: str):
    model = _get_model()
    for chunk in model.stream([HumanMessage(content=prompt)]):
        if chunk.content:
            yield chunk.content
