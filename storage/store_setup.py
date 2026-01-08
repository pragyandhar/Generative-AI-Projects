# It configures the short-term-memory and long-term-memory so the agent remembers the current conversation and user-specific settings

from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver

def initialize_storage():
    """
    Initialise both short-term (checkpointer) and Long-term (Store) memory.
    """

    # 1. Short Term Memory (per thread)
    checkpointer = InMemorySaver()

    # 2. Long Term Memory (across threads)
    store = InMemoryStore()

    return checkpointer, store