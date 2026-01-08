# Tools for HR Department

from langchain.tools import tool, ToolRuntime
from config.schema import SentinelContext

@tool
def get_employee_handbook(query: str, runtime: ToolRuntime[SentinelContext]) -> str:
    """
    Search the employee handbook for policies and benefits
    """
    ctx = runtime.context
    
    if ctx.clearance_level >= 2:
        return f"Results for '{query}': [Policy 402: Bonus Structures, Policy 101: Conduct]"
    else:
        return f"Results for '{query}': [Policy 101: Conduct]"
    
@tool
def get_my_payroll_status(runtime: ToolRuntime[SentinelContext]) -> str:
    """Fetch each employee's payroll status from the HR Database"""
    user_id = runtime.context.user_id
    return f"Payroll Record for {user_id}: [Status: Paid, Last_Date: 2026-01-01]"