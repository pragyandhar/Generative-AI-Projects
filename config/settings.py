# Centralizes model selection (e.g., choosing GPT-4o for the brain and GPT-4o-mini for guardrails) and loads API keys.

import os
from langchain.chat_models import init_chat_model

# --- MODEL CONFIGURATIONS --- #
PRIMARY_MODEL_NAME = "gpt-4o"
SECONDARY_MODEL_NAME = "gpt-4o-mini"

def get_primary_model():
    return init_chat_model(PRIMARY_MODEL_NAME, temperature=0)

def get_secondary_model():
    return init_chat_model(SECONDARY_MODEL_NAME, temperature=0)