# Sensitive Tools which require human to approve (Human-in-the-loop)

from langchain.tools import tool, ToolRuntime
from config.schema import SentinelContext

@tool
def list_server_status(runtime: ToolRuntime[SentinelContext]) -> str:
    """
    Check the health of all internal servers. Safe to Run without Approval.
    """
    # Example of RBAC inside the tool
    if runtime.context.department != "IT":
        return "ACCESS DENIED: Only IT professionals can view server health"
    
    return "All Systems Operational: [DB-01: OK, API-01: OK, WEB-04: OK]" # Some example systems

@tool
def restart_server(server_id: str, runtime: ToolRuntime[SentinelContext]) -> str:
    """
    Restart a specific server.
    DANGER: This tool will be interrupted by Human-in-the-Loop middleware.
    """

    # Even if the agent tries to call this, the HITL middleware will pause it for human approval
    return f"SUCCESS: Server {server_id} has been rebooted by {runtime.context.user_name}."
