# It contains the dataclass definitions for your Runtime Context. By defining the schema here, you ensure that every tool and middleware knows exactly what data (like user_id or clearance_level) is available during execution.

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class SentinelContext:
    """This is the Runtime Context for SentinelNexus. It only contains the definition of schema variables"""

    # User Identity
    user_id: str
    user_name: str

    # Organisational Context
    department: str
    clearance_level: str # If clearance_level < 3, your middleware will physically block the model from calling tools that access sensitive data.

    # Multi-tenancy & Environment
    tenant_id: str = "sentinel_corp_global"
    deployment_env: str = "production"

    # Session Metadata
    session_id: Optional[str] = None
    request_id: Optional[str] = None

    # Audit & Compliance Flags
    is_audit_enabled: bool = True
    compliance_frameworks: List[str] = field(default_factory=lambda:["GDPR", "SOC2"])

    def to_dict(self) -> Dict[str, Any]:
        """Method to convert context to dictionary for logging"""
        return {
            "user": self.user_id,
            "dept": self.department,
            "clearance": self.clearance_level,
            "env": self.deployment_env,
            "tenant": self.tenant_id
        }