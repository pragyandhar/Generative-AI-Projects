# SentinelNexus: Enterprise-Grade AI Agent with Compliance & Security

A production-ready, multi-tenant AI agent built with LangChain and LangGraph that integrates compliance frameworks, role-based access control, and advanced middleware orchestration. Designed for enterprise environments where security, auditability, and context awareness are non-negotiable.

---

## Project Overview

SentinelNexus demonstrates advanced patterns in AI engineering that go far beyond simple chatbot implementations. This is a system designed for real-world deployment in regulated industries where:

- User identity and clearance levels directly influence LLM behavior
- Personally identifiable information (PII) is automatically masked before reaching the model
- Tool execution requires human approval based on risk assessment
- Conversation history is intelligently summarized to prevent context overload
- Every interaction is logged for compliance audit trails
- Response content is validated against user clearance before being delivered

### Key Differentiators

Unlike typical AI applications, SentinelNexus implements **Defense in Depth** security through a carefully orchestrated middleware pipeline that operates at five distinct layers:

1. **PII Protection** (Input/Output): Deterministic regex-based masking and blocking
2. **Dynamic Prompt Engineering** (Context): Runtime-aware system prompts that adapt to user identity
3. **Memory Management** (State): Automatic conversation summarization to prevent degradation
4. **Human Approval Gate** (Workflow): Sensitive tool execution requires human intervention
5. **Safety Validation** (Output): LLM-based semantic checking against clearance levels

---

## Architecture & Design Patterns

### Core Components

#### 1. Runtime Context Schema (`config/schema.py`)

The `SentinelContext` dataclass is the foundation of the entire system:

```python
@dataclass
class SentinelContext:
    user_id: str
    user_name: str
    department: str  # Finance, IT, HR, etc.
    clearance_level: int  # 1-5 scale
    tenant_id: str
    deployment_env: str
    is_audit_enabled: bool
    compliance_frameworks: List[str]  # ["GDPR", "SOC2", "SOX", "HIPAA"]
```

**Why This Matters:**

- **Type Safety**: Using a dataclass eliminates "dictionary hell" and prevents key typos
- **Compliance Automation**: The `compliance_frameworks` list allows middleware to automatically inject legal disclaimers into prompts
- **Access Control**: The clearance-level acts as the core logic for guardrails. If `clearance_level < 3`, the agent is physically blocked from calling tools accessing sensitive data
- **Auditability**: The `to_dict()` method ensures every LLM call can be logged with full context, creating a forensic trail if hallucinations occur

#### 2. Dynamic Prompt Engineering (`middleware/prompts.py`)

The system uses context-aware prompt construction rather than static prompts:

**Four-Block Architecture:**

- **Block A - Base Identity**: Today's date, corporate persona, user identity, and security commitment
- **Block B - Department-Specific Protocols**: Department determines instructions (Finance gets SOX compliance rules, IT gets technical CLI guidance, HR gets GDPR reminders)
- **Block C - Personalization from Long-Term Memory**: Fetches user preferences (expertise level, communication style) from the Store
- **Block D - Efficiency Logic**: If conversation is >10 messages, agent becomes more concise
- **Block E - Compliance Warnings**: If GDPR is active, footer about privacy is injected

**Technical Innovation**: This is not prompt injection—it's intentional, validated **context engineering**. Each block is conditionally applied based on runtime state, reducing token waste and preventing LLM confusion.

**Key Concepts Explained:**
- **ModelRequest**: A typed request object passed to the dynamic_prompt function containing request context, messages, and runtime state
- **tenant_id**: Ensures multi-tenant isolation. Tools validate this to prevent data leakage between customers
- **SOX Compliance Standards**: Sarbanes-Oxley requirements for financial reporting accuracy and audit trails
- **Need-to-Know Policy**: Information access restricted to only those requiring it for their role
- **GDPR Guidelines**: EU data protection regulations requiring explicit consent, data minimization, and privacy notices

The line `return "\n".join(prompt_blocks)` concatenates all conditional blocks into a single system prompt string, preserving newlines for readability.

#### 3. Multi-Layer Guardrails (`middleware/guardrails.py`)

**Layer 1: Deterministic PII Protection**

Uses regex-based middleware to:
- Mask email addresses before LLM sees them
- Block credit card numbers entirely
- Redact API keys using pattern `sk-[a-zA-Z0-9]{32}`

**Layer 2: Semantic Safety Checking**

After the agent produces a response:
1. If user clearance < 3, invoke a secondary model (gpt-4o-mini for cost efficiency)
2. Check response for "confidential" words, executive salaries, password hints
3. If unsafe, replace with `[SECURITY ALERT]` and jump to end node
4. Otherwise, pass through

**Key Innovation**: The guardrail doesn't just block everything—it's **context-aware**. A Level 5 executive can see financial data; a Level 1 intern cannot. This prevents false positives while maintaining security.

**Understanding Runtime[SentinelContext]:**
- This is a generic type indicating the runtime carries a context of type SentinelContext
- The `after_agent` hook receives the runtime as a parameter, allowing access to `runtime.context`
- The agent's final response is intercepted after the LLM creates it but before it's returned to the user
- This placement allows semantic validation without the main model needing to know about it

#### 4. Memory Management (`middleware/logic.py`)

Implements conversation summarization to prevent **Context Overload Failure**:

- Trigger: When conversation hits 15 messages OR 4000 tokens
- Keep: Last 5 messages in full detail for immediate context
- Summarize: Everything before that into transaction IDs and key decisions
- Model: gpt-4o-mini (cost-optimized)

**Real-World Problem Solved**: A 30+ message conversation can cause LLMs to ignore system prompt rules. This middleware ensures the agent never loses "mode awareness."

#### 5. Dependency Injection via ToolRuntime (`tools/*.py`)

Each tool receives its own runtime context:

```python
@tool
def get_revenue_report(quarter: str, runtime: ToolRuntime[SentinelContext]) -> str:
    ctx = runtime.context
    if ctx.department != "Finance":
        return "ACCESS DENIED"
    if ctx.clearance_level < 3:
        return "RESTRICTED: Need Clearance Level 3"
    return actual_data
```

**Why This Pattern:**

- The tool "knows" who is calling it without the LLM passing a user_id string (which could be prompt-injected)
- Role-Based Access Control (RBAC) lives in the tool layer, not the LLM layer
- If the agent tries to circumvent access rules through creative prompting, it fails at the tool boundary

**Typing Library Usage Explained:**
- `Dict[str, Any]`: Dictionary with string keys and values of any type (flexible but still typed)
- `List[str]`: List containing only strings (enforces homogeneity)
- `Optional[str]`: String that can be None (proper null handling)
- `ToolRuntime[SentinelContext]`: Generic type indicating the runtime carries SentinelContext
- These enable IDE autocomplete, static type checking, and documentation generation

#### 6. Agent Assembly & Pipeline (`agent.py`)

The agent brings all components together in a carefully ordered pipeline:

```
User Input
    ↓
[PII Masking] ← Layer 1: Deterministic protection
    ↓
[Dynamic Prompt] ← Layer 2: Context Engineering
    ↓
[Summarization] ← Layer 3: Memory Management
    ↓
[LLM Model]
    ↓
[Tool Execution with RBAC]
    ↓
[Human-in-the-Loop Gate] ← Layer 4: Approval for sensitive tools
    ↓
[Safety Guardrail] ← Layer 5: Final semantic check
    ↓
User Output
```

**Pipeline Order Matters:**
- PII masking comes first so downstream middleware doesn't see raw data
- Dynamic prompt comes early so context engineering shapes LLM reasoning
- Safety guardrail comes last so it validates the final output

#### 7. Short & Long-Term Memory (`storage/store_setup.py`)

- **Short-Term (Checkpointer)**: InMemorySaver tracks conversation within a thread. Enables Human-in-the-Loop workflows (agent pauses, waits for approval, resumes)
- **Long-Term (Store)**: InMemoryStore holds user preferences across threads. Future expansion: Redis for multi-instance deployments

---

## Streamlit Frontend (`app.py`)

The UI orchestrates the agent with production-grade patterns:

### Security Features

- **Ephemeral API Key Handling**: OpenAI API key stored only in Streamlit session state
- **Auto-Flush on Close**: Refreshing the browser tab or closing clears the key and all state
- **Lazy Agent Loading**: Agent import deferred until API key is present, preventing initialization errors
- **Cache Management**: Agent cached but cleared on key reset

### Real-Time Context Configuration

Sidebar controls allow operators to dynamically set:
- User identity (ID, name, department)
- Clearance level (1-5 slider)
- Tenant and environment (production/staging/dev)
- Compliance frameworks to activate
- Audit logging toggle

### Chat Interface

- Messages are preserved in session state
- Streaming execution via `.stream()` method to handle tool calls properly
- Error messages include truncated details for debugging
- Thread ID persists for checkpointing across interactions

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Web UI for agent interaction |
| **Core Agent** | LangChain, LangGraph | Multi-step agentic reasoning |
| **LLM** | OpenAI GPT-4o (primary), GPT-4o-mini (guardrails) | Language model backbone |
| **Memory** | InMemorySaver, InMemoryStore | Short/long-term state management |
| **Middleware** | Custom Python classes | PII, prompts, summarization, approval gates |
| **Tools** | Decorated Python functions with ToolRuntime | Department-specific utilities |

---

## Use Cases

### 1. Financial Services Compliance

An analyst in the Finance department asks: "What was Q3 revenue?"

- **Prompt Engineering**: System injects "Apply SOX compliance standards to all data reporting" + "Include transaction timestamps"
- **Access Control**: Revenue tool checks `ctx.department == "Finance"` and `ctx.clearance_level >= 3`
- **PII Protection**: Any employee names in the data are masked before LLM output
- **Audit Trail**: Query logged with user ID, timestamp, clearance level

### 2. IT Operations with Approval Gates

An engineer asks: "Restart server DB-01 to fix the latency issue."

- **Human-in-the-Loop**: Agent generates response but pauses before executing restart_server
- **Approval Workflow**: Human reviews the request via Streamlit UI, approves or denies
- **Memory Preservation**: Agent remembers context while waiting (checkpointer enables this)
- **Execution**: Only after approval does the tool run; result is logged

### 3. Multi-Tenant SaaS Isolation

Two companies, TenantA and TenantB, both use SentinelNexus:

- Each user's `tenant_id` is captured in context
- Tools can validate: `if ctx.tenant_id != expected_tenant: return "Access Denied"`
- Long-term store can partition by tenant
- Audit logs show clear tenant boundaries

---

## Why This Approach Matters

### For Enterprises

This is not a fun demo. It's enterprise architecture:
- Every interaction is auditable (context logged with each call)
- Security is enforced at multiple layers (defense in depth)
- Compliance frameworks are baked in, not bolted on
- Human approval gates prevent autonomous financial/operational damage

### For AI Engineers

This showcases patterns that scale:
- **Middleware Abstraction**: New safety rules don't require retraining the LLM
- **Context as a First-Class Citizen**: User identity shapes behavior everywhere
- **Graceful Degradation**: If the safety check fails, the user still gets an informative response
- **Tool-Level RBAC**: Authorization lives where the data lives, not in the LLM

### For Recruiters

This demonstrates:
- Ability to architect systems beyond "prompt → LLM → response"
- Understanding of compliance, security, and auditability in AI
- Production-ready patterns (lazy loading, caching, error handling)
- Full-stack capability (backend logic + frontend UI)

---

## Deployment & Scalability

### Current (Development)

- In-memory storage for prototyping
- Single Streamlit instance
- OpenAI API calls direct from app

### Future (Production)

```
Streamlit App → FastAPI Service
    ↓
LangGraph Agent Graph
    ↓
PostgreSQL (Checkpointer)
Redis (Long-term Store)
    ↓
OpenAI, Custom Tools, External APIs
```

Key scaling decisions:
- Move memory backends from in-memory to persistent stores
- Separate the agent into a service for multi-client access
- Implement queue-based tool execution for long-running tasks
- Add comprehensive monitoring/observability

---

## Development & Contributions

### Backend Architecture (Written by Pragyan Dhar)

The backend implements the entire middleware pipeline and agent logic:
- Context schema and validation
- Middleware components (PII, prompts, safety, summarization)
- Tool definitions with RBAC
- Storage initialization and management
- Agent assembly and configuration

### Frontend Application (Built by AI Assistant)

The Streamlit app provides:
- Responsive, intuitive UI for agent interaction
- Real-time configuration of runtime context
- Secure API key handling
- Stream-based response rendering
- Error tracking and debugging

---

## Project Structure

```
.
├── app.py                       # Streamlit frontend (AI-built)
├── agent.py                     # Agent assembly & pipeline orchestration
├── config/
│   ├── schema.py               # SentinelContext dataclass
│   └── settings.py             # Model initialization
├── middleware/
│   ├── guardrails.py           # PII protection + safety checks
│   ├── prompts.py              # Dynamic prompt engineering
│   └── logic.py                # Summarization middleware
├── storage/
│   └── store_setup.py          # Memory backends initialization
├── tools/
│   ├── finance_tools.py        # Revenue reports, invoice status
│   ├── hr_tools.py             # Handbook, payroll queries
│   └── it_tools.py             # Server status, restart (HITL)
└── requirements.txt            # Dependencies
```

---

## Installation & Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key (GPT-4o access required)

### Setup

```bash
git clone <repository>
cd Generative-AI-Projects

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

1. Open browser to `http://localhost:8501`
2. Paste OpenAI API key in the sidebar
3. Configure identity and clearance level
4. Start chatting—watch middleware in action

---

## Key Learnings & Advanced Patterns

### 1. Context Engineering Over Prompt Injection

Rather than trying to inject context into the prompt string unsafely, we:
- Define a typed schema (`SentinelContext`)
- Pass it through the runtime (not the input)
- Middleware reads it and generates prompts deterministically

**Result**: No prompt injection attacks, type-safe, auditable.

### 2. Tool-Level Authorization

RBAC doesn't live in the LLM; it lives at the tool boundary:
- Tool receives `ToolRuntime[SentinelContext]`
- Tool checks clearance level before returning data
- If LLM tries to circumvent via creative prompting, tool refuses

**Result**: Authorization is enforceable, not advisory.

### 3. Multi-Layer Safety

We don't rely on a single safety mechanism:
- Regex blocks known PII patterns (fast)
- Secondary LLM checks semantic safety (thorough)
- Tool-level checks prevent unauthorized access (enforceable)

**Result**: Defense in depth prevents single-point failures.

### 4. Memory as a First-Class Concern

Without the summarization middleware, long conversations cause:
- Token bloat (expensive)
- Context degradation (LLM ignores system rules)
- State loss (agent "forgets" its mode)

By managing conversation length actively, we preserve agent behavior across long interactions.

### 5. Human-in-the-Loop as a Workflow Pattern

Rather than having a human manually approve outputs, we:
- Let agent reason and decide to call the tool
- Middleware intercepts sensitive tools and pauses
- Human approves or denies with full context
- Agent resumes exactly where it left off

**Result**: Automation + human oversight without losing agent continuity.

---

## License

Open source. Feel free to use for learning and projects.

---

## Contact & Credits

**Backend Architecture & Implementation**: Pragyan Dhar

**Frontend Application & UI/UX**: AI Assistant

For questions about the system architecture, deployment patterns, or AI engineering best practices, this project serves as a practical reference for production-grade agent development.

---

## Appendix: Why This Matters

Most AI applications today are: prompt → LLM → output. SentinelNexus is fundamentally different because it treats user identity, compliance requirements, and security as first-class citizens in the system architecture.

This is not a toy. It's a template for building AI systems that enterprises can actually deploy in regulated industries.
