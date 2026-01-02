# IMPORTS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from structured import get_lesson
from quiz_generator import quiz_generator
from math_solver import solve_math
from wikipedia import wikipedia_lookup
from analytics import get_token_and_logprob_metrics

import pprint
import redis
import hashlib

# API KEY
api_key = ""

# PROMPT
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            """You are an expert AI Tutor. You specialize in all the subjects and topics around the world. You are polite and very humble in your language. You have the most masculine energy in the world.

            You have to answer this question of the user with your experience and understanding. Break it down into steps so that the concept is clear in the user's mind. Use as less words for explanation as possible.
            Give real-life examples after and also understand the summary of your response and generate a quiz of 5 questions increasing in difficulty.
            """
        ),
        (
            "human", "{question}"
        )
    ]
)

# MODEL
llm = ChatOpenAI(
    model = "gpt-4o-mini",
    api_key = api_key,
    temperature = 0.5,
    max_completion_tokens = 2000
)

# BINDING THE IMPORTED TOOLS 
agent_with_tools = llm.bind_tools([quiz_generator, solve_math, wikipedia_lookup])

# CHAIN OF PROMPT AND MODEL
chain = prompt_template | agent_with_tools

# cache context signature to prevent key collisions when model/prompt/tools change
PROMPT_SIGNATURE = hashlib.sha256(str(prompt_template).encode()).hexdigest()
TOOL_SIGNATURE = "quiz_generator|solve_math|wikipedia_lookup"
CACHE_CONTEXT = {
    "model": llm.model,
    "temperature": llm.temperature,
    "prompt": PROMPT_SIGNATURE,
    "tools": TOOL_SIGNATURE,
}

# RUNNING THE CHAIN

# prompt caching with redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True) # connect to redis

def get_cache_key(question: str):
    """
    It craetes a cache key for identification purposes
    """
    # combine model/prompt/tools/question so cache keys change when config changes
    payload = "|".join(
        [
            CACHE_CONTEXT["model"],
            str(CACHE_CONTEXT["temperature"]),
            CACHE_CONTEXT["prompt"],
            CACHE_CONTEXT["tools"],
            question,
        ]
    )
    return hashlib.sha256(payload.encode()).hexdigest()

def basic_invocation(question: str):
    """
    Get response in a unstructed format - A plain text answer. It also includes prompt caching with redis
    """
    key = get_cache_key(question=question) # make a key

    # check if cache found - if yes then return the cache else run the model
    cached = r.get(key)
    if cached:
        return cached

    response = chain.invoke({"question": question})
    ans = response.content

    r.set(key, ans, ex=3600) # set expiration of the key-value pair in cache for 1 hour (3600s)

    return ans

def structured_response(question: str):
    """
    Get structured responses
    """
    raw_text = basic_invocation(question=question)
    structured_output = get_lesson(raw_text)
    return structured_output

def streaming_response(question: str):
    key = get_cache_key(question=question)
    cached = r.get(key)
    if cached:
        return cached

    stream = chain.stream({"question": question})
    full = ""
    for chunk in stream:
        print(chunk.content, end="", flush=True)
        full += chunk.content

    # store streamed result
    r.set(key, full, ex=3600)
    return full

# TESTING THE RESPONSES
if __name__ == "__main__":
    prompt = "Explain gravity in simple terms"
    metrics = get_token_and_logprob_metrics(prompt)

    # 1. Print the text response
    print(f"Text Response: \n{metrics['text']}\n")

    # 2. Print Token Usage
    print("-" * 30)
    print(f"Input Tokens:  {metrics['input_tokens']}")
    print(f"Output Tokens: {metrics['output_tokens']}")
    print(f"Total Tokens:  {metrics['total_tokens']}")

    # 3. Print Response Time
    print(f"Response Time: {metrics['duration_seconds']} seconds")

    # 4. Print Logprobs 
    print("-" * 30)
    print("Logprobs for the first 2 tokens:")

    first_token = metrics["logprobs_data"][:1] 

    for item in first_token:
        # Each item is a list of top candidates for that position
        chosen = item[0]
        print(f"Token: '{chosen['token']}' | Logprob: {chosen['logprob']}")
