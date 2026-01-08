# This file imports the LLM, the tools, and the middleware. Its sole job is to call create_agent() and configure how the LangGraph runtime should execute.

# --- IMPORTS --- #
# 1. Langchain Core & Runtime Imports
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
# 2. Project-Specific Imports
from config.schema import SentinelContext
from config.settings import get_primary_model
from storage.store_setup import initialize_storage
from middleware.prompts import dynamic_prompt_system
from middleware.guardrails import pii_army, SafetyGuardrailMiddleware
from middleware.logic import get_summarisation_middleware
# 3. Import all tool sets
from tools.it_tools import list_server_status, restart_server
from tools.hr_tools import get_employee_handbook, get_my_payroll_status
from tools.finance_tools import get_revenue_report, check_invoice_status
# --- IMPORTS --- #

def create_sentinel_agent():
    """
    Assembles the SentinelNexus agent with all middleware and tools
    """

    # 1. Initialise the Brain and Storage
    llm = get_primary_model()
    checkpointer, store = initialize_storage()

    # 2. Define HITL Shield
    human_in_the_loop = HumanInTheLoopMiddleware (
        interrupt_on = {
            "restart_server": True,           
            "get_revenue_reports": True,
            "get_my_payroll_status": False,
            "check_invoice_status": False
        }
    )

    # 3. Define complete middleware pipeline
    middleware_pipeline = [
        *pii_army,                      # LAYER-1: PII Masking/Redaction
        dynamic_prompt_system,          # LAYER-2: Context Engineering
        get_summarisation_middleware(), # LAYER-3: Memory Management
        human_in_the_loop,              # LAYER-4: Human Approval
        SafetyGuardrailMiddleware()     # LAYER-5: Output Validation
    ]

    # Combining all the tools
    all_tools = [
        list_server_status,
        restart_server,
        get_employee_handbook,
        get_my_payroll_status,
        get_revenue_report,
        check_invoice_status,
        get_my_payroll_status
    ]

    # Assemble the Agent
    agent = create_agent (
        model = llm,
        tools = all_tools,
        middleware = middleware_pipeline,
        context_schema = SentinelContext,
        checkpointer = checkpointer,       # Enables Short Term Memory and HITL
        store = store                      # Enables Long Term Memory  
    )

    return agent

sentinel_agent = create_sentinel_agent()