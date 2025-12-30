# IMPORTING LIBRARIES
import os
import getpass

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain.messages import SystemMessage

from typing import Dict, List, Any

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# Create the custom state - create a strict control variable and extends LangChain's states
class LiteraryState(AgentState) :
    allowed_domain = str

# Creating a middleware
def DomainEnforcementMiddleware(AgentMiddleware) :
    state_schema = LiteraryState

    def before_model(self, state: LiteraryState, runtime) -> dict[str, Any] | None:
        last_message = state.messages[-1]['content'].lower()
        allowed = state.allowed_domain.lower()

        if allowed not in last_message:
            return {
                "messages": [
                    {
                        "role" : "assistant",
                        "content" : f"This agent only answers the messages for {state.allowed_domain} domain. Please ask inside this domain only",
                    }
                ]
            }

# Sets tone, role and behavior of the agent
system_prompt = SystemMessage(
    content=(
        "You are a literary analysis assistant.\n"
        "Your task is to analyze and explain concepts strictly related to a single literary work.\n"
        "Respond concisely, with clear literary reasoning.\n"
        "Do not speculate beyond the provided work."
    )
)

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1, # not creative
    max_tokens=1000,
    timeout=30
)

agent = create_agent(
    model = model,
    system_message = system_prompt,
    state_schema = LiteraryState,
    middleware = [DomainEnforcementMiddleware()]
)