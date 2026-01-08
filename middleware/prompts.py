# Contains @dynamic_prompt functions. Its responsibility is to look at the Runtime Context and the Storeto rewrite the system prompt quickly before the LLM sees it.

import datetime
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from config.schema import SentinelContext

@dynamic_prompt
def dynamic_prompt_system(request: ModelRequest) -> str:
    """
    This is the context engineering function
    It dynamically constructs a system prompt by merging Runtime Context, State and Store data
    """

    # 1. Access Runtime Context (the "who")
    ctx: SentinelContext = request.runtime.context

    # 2. Access State (the "current situation")
    message_count = len(request.messages)

    # 3. Access the Store (the "History")
    user_preference = {}
    if request.runtime.store:
        saved_pref = request.runtime.store.get(("users", ctx.user_id), "preferences")
        if saved_pref:
            user_preference = saved_pref.value
    
    # --- BLOCK A: Base Identity & Corporate Persona --- #
    today = datetime.date.today().strftime("%B %d, %2026")
    prompt_blocks = [
        f"Today is {today}.",
        f"You are SentinelNexus, a highly secure AI Agent for the {ctx.tenant_id} ecosystem.",
        f"Current User: {ctx.user_name} | Department: {ctx.department} | Clearance: Level {ctx.clearance_level}.",
        "Your goal is to provide accurate, department-specific assistance while maintaining strict security."
    ]

    # --- BLOCK B: Department-Specific Context (Context Engineering) --- #
    if ctx.department == "Finance":
        prompt_blocks.append(
            "\n[FINANCE PROTOCOLS]"
            "\n- Apply SOX compliance standards to all data reporting."
            "\n- You must provide currency figures in USD and include transaction timestamps."
            "\n- If asked for sensitive tax IDs, remind the user of the 'Need-to-Know' policy."
        )
    elif ctx.department == "IT":
        prompt_blocks.append(
            "\n[TECHNICAL OPS PROTOCOLS]"
            "\n- Focus on technical accuracy. Provide CLI commands in code blocks."
            "\n- You have permission to suggest server restarts, but NOT to execute them without approval."
        )
    elif ctx.department == "HR":
        prompt_blocks.append(
            "\n[PEOPLE OPS PROTOCOLS]"
            "\n- Use an empathetic but professional tone."
            "\n- Strictly follow GDPR and PII guidelines. Never repeat an employee's private ID."
        )
    
    # --- BLOCK C: Personalization from Long-Term Memory (Store) --- #
    if user_preference:
        style = user_preference.get("style", "professional")
        expertise = user_preference.get("expertise_level", "general")
        prompt_blocks.append(
            f"\n[USER PREFERENCES]\n- Adjust your technical depth to '{expertise}' level."
            f"\n- The user prefers a '{style}' communication style."
        )
    
    # --- BLOCK D: Efficiency Logic (State Awareness) --- # 
    if message_count > 10:
        prompt_blocks.append(
            "\n[EFFICIENCY NOTE]\n- This conversation is getting long. Be extra concise in your summaries."
        )
    
    # --- BLOCK E: Compliance Warnings (Runtime Flags) --- $
    if "GDPR" in ctx.compliance_frameworks:
        prompt_blocks.append("\n- MANDATORY: Include a privacy footer if personal data is discussed.")

    return "\n".join(prompt_blocks)
