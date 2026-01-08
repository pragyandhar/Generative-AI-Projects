# Handles Life-cycle Context. Its main responsibility is to Summarize.

from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model

def get_summarisation_middleware():
    """
    Returns a middleware that triggers summarisation when the conversation history hits specific limit
    """
    return SummarizationMiddleware(
        # Define the model
        model = init_chat_model("gpt-4o-mini"),

        # Trigger when the history reaches 15 messages or 4000 tokens
        trigger=[
            ("messages", 15),
            ("tokens", 4000)
        ],

        # Keep the last 5 messages in full detail for immediate context
        keep = ("messages", 5),

        summary_prompt="Summarize the core request and technical context of the following enterprise support conversation. Maintain all transaction IDs."
    )