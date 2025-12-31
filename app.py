from fastapi import FastAPI
from models import invoke_model, stream_model
from tools import weather_agent
from structured import structured_summary
from analytics import get_logprobs

app = FastAPI()

@app.get("/invoke")
def invoke(q: str):
    return invoke_model(q)

@app.get("/stream")
def stream(q: str):
    return stream_model(q)

@app.get("/weather")
def weather(q: str):
    return weather_agent(q)

@app.get("/summary")
def summary(q: str):
    return structured_summary(q)

@app.get("/logprobs")
def logprobs(q: str):
    return get_logprobs(q)
