# It performs the safety checks for input and output

import re
from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config, PIIMiddleware
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langchain.chat_models import init_chat_model
from config.schema import SentinelContext

# --- 1. Deterministic Guardrails: PII Protection --- #
# Run this automatically on every message before the LLM sees them
pii_army = [
    PIIMiddleware(
        pii_type="email",
        strategy="mask",
        apply_to_input=True,
        apply_to_output=True
    ),
    PIIMiddleware(
        pii_type="credit_card",
        strategy="block",
        apply_to_input=True
    ),
    PIIMiddleware(
        pii_type="api_key",
        detector=r"sk-[a-zA-Z0-9]{32}",
        strategy="redact",
        apply_to_input=True
    )
]

# --- 2. Model-Based Guardrails: Compliance & Safety --- #
class SafetyGuardrailMiddleware(AgentMiddleware):
    """
    An after-agent guardrail that matches the user's final response to ensure it matches the user's clearance level
    """

    def __init__(self):
        super().__init__()
        self.checker_model = init_chat_model("gpt-4o-mini")

    @hook_config(can_jump_to=["end"])
    def after_agent(self, state: AgentState, runtime: Runtime[SentinelContext]) -> dict[str, Any] | None:
        """
        Runs just once after the agent has decided on its final response.
        """
        ctx = runtime.context

        # Get the final AI response
        if not state["messages"]:
            return None
        
        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return None
        
        # Logic: If clearance is low, check for "confidential" words
        if ctx.clearance_level < 3:
            check_prompt = f"""
            You are a Security Auditor. 
            Evaluate if the following AI response contains restricted internal passwords, 
            executive salaries, or 'Confidential' project names.
            
            Response: {last_message.content}
            
            Reply ONLY with 'SAFE' or 'UNSAFE'.
            """

            audit_result = self.checker_model.invoke([
                {
                    "role": "user",
                    "content": check_prompt
                }
            ])

            if "UNSAFE" in audit_result.content.upper():
                # Overwrite the message and end its execution
                return {
                    "message": [
                        AIMessage(content="[SECURITY ALERT] My response was blocked because it contained "
                                          "information above your current clearance level.")
                    ],
                    "jump_to": "end"
                }
            
        return None