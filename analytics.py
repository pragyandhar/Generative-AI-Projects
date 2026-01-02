# IMPORTING
import time
from openai import OpenAI

# API KEY
client = OpenAI(api_key="")

def get_token_and_logprob_metrics(prompt: str):
    start = time.time()

    # Call OpenAI to get logarithmic probabilities
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        # getting top-5 logarithmic probabilities distinct words
        logprobs=True,
        top_logprobs=5
    )

    duration = time.time() - start

    usage = resp.usage
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    # Extract logprobs from new structure
    choices = resp.choices
    logprob_data = []

    for choice in choices:
        if choice.logprobs and choice.logprobs.content:
            token_logprobs = [
                # Each item in 'content' has a 'top_logprobs' list
                {
                    "token": item.token,
                    "logprob": item.logprob,
                    "top5": [
                        {
                            "token": top.token, 
                            "top_logprob": top.logprob
                        }
                        for top in item.top_logprobs
                    ]
                }
                for item in choice.logprobs.content
            ]
            logprob_data.append(token_logprobs)
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "logprobs_data": logprob_data, # Renamed for clarity
        "duration_seconds": round(duration, 3),
        "text": resp.choices[0].message.content
    }