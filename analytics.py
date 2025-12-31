import os
from openai import OpenAI

def get_logprobs(prompt: str):
    """Lazy initialization of OpenAI client"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        logprobs=True,
        top_logprobs=5
    )
    return {
        "content": resp.choices[0].message.content,
        "logprobs": resp.choices[0].logprobs
    }