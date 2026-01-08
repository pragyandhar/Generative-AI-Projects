# Tools for Financial Data and Reports

from langchain.tools import tool, ToolRuntime
from config.schema import SentinelContext

@tool
def get_revenue_report(quarter: str, runtime: ToolRuntime[SentinelContext]) -> str:
    """Fetch the corporate revenue report for a specific quarter."""
    ctx = runtime.context
    
    # AUTHENTICATION: Department-level check using Runtime
    if ctx.department != "Finance":
        return f"ACCESS DENIED: User {ctx.user_name} is not authorized to view Finance data."
    
    # AUTHORIZATION: Clearance-level check
    if ctx.clearance_level < 3:
        return "RESTRICTED: You need Clearance Level 3 to view full revenue reports."
        
    return f"REVENUE REPORT (Q{quarter}): Total Revenue: $5.2M | Growth: +12% | Status: Healthy."

@tool
def check_invoice_status(invoice_id: str, runtime: ToolRuntime[SentinelContext]) -> str:
    """Check the payment status of an invoice."""
    # Finance and IT both might need this, so we check for both
    if runtime.context.department not in ["Finance", "IT"]:
        return "Access Denied: Please contact the billing department."
        
    return f"Invoice {invoice_id}: [Status: PAID] [Date: 2026-01-05] [Amount: $1,200]"