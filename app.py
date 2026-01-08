import os
import uuid
from typing import List

import streamlit as st
from langchain.messages import AIMessage, HumanMessage

from config.schema import SentinelContext


# --- Page Setup --- #
st.set_page_config(
	page_title="SentinelNexus Control Room",
	layout="wide",
	initial_sidebar_state="expanded",
)


# --- Session Bootstrapping --- #
def clear_state():
	"""Reset chat, context, and in-memory API key."""
	st.session_state.pop("lc_messages", None)
	st.session_state.pop("session_id", None)
	st.session_state.pop("api_key", None)
	os.environ.pop("OPENAI_API_KEY", None)
	try:
		get_sentinel_agent.clear()
	except Exception:  # noqa: BLE001
		pass


@st.cache_resource(show_spinner=False)
def get_sentinel_agent():
	"""Lazy-load the agent only after the API key is present to avoid import-time errors."""
	# Import inside to ensure OPENAI_API_KEY is available
	from agent import sentinel_agent as base_agent  # type: ignore

	return base_agent


if "lc_messages" not in st.session_state:
	st.session_state.lc_messages: List = []
if "session_id" not in st.session_state:
	st.session_state.session_id = str(uuid.uuid4())


# --- Sidebar: Security & Context --- #
with st.sidebar:
	st.title("Session Controls")

	st.markdown("#### API Key")
	api_key = st.text_input(
		"OpenAI API Key",
		type="password",
		help=(
			"Key is stored only in this browser tab via session state. "
			"Refreshing or closing the tab clears it."
		),
	)

	if api_key:
		st.session_state.api_key = api_key
		os.environ["OPENAI_API_KEY"] = api_key
	else:
		st.session_state.pop("api_key", None)
		os.environ.pop("OPENAI_API_KEY", None)

	st.button("Flush key and reset session", on_click=clear_state, use_container_width=True)

	st.markdown("---")
	st.markdown("#### Identity & Access")
	user_id = st.text_input("User ID", value="u-1001")
	user_name = st.text_input("User Name", value="Enterprise Analyst")
	department = st.selectbox("Department", ["Finance", "IT", "HR", "Other"], index=1)
	clearance_level = st.slider("Clearance Level", min_value=1, max_value=5, value=3)

	st.markdown("---")
	st.markdown("#### Tenant & Compliance")
	tenant_id = st.text_input("Tenant ID", value="sentinel_corp_global")
	deployment_env = st.selectbox("Environment", ["production", "staging", "dev"], index=0)
	compliance_frameworks = st.multiselect(
		"Compliance Frameworks",
		["GDPR", "SOC2", "SOX", "HIPAA"],
		default=["GDPR", "SOC2"],
	)
	is_audit_enabled = st.toggle("Audit Logging Enabled", value=True)

	st.markdown("---")
	st.caption(
		"Human-in-the-loop will pause sensitive tools. Guardrails enforce clearance-aware responses."
	)


# --- Layout: Hero / Status --- #
st.title("SentinelNexus Control Room")
st.markdown(
	"Operate the enterprise-grade, compliance-aware agent. Configure identity, guardrails, and chat in real time."
)

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Tenant", tenant_id)
col_b.metric("Environment", deployment_env)
col_c.metric("Clearance", f"Level {clearance_level}")
col_d.metric("Audit Trail", "On" if is_audit_enabled else "Off")

with st.expander("Execution Blueprint", expanded=False):
	st.markdown(
		"- PII shield before model input/output\n"
		"- Dynamic prompt conditioned on runtime context and preferences\n"
		"- Summarization middleware for long threads\n"
		"- Human-in-the-loop for sensitive tools\n"
		"- Safety guardrail validating final responses against clearance"
	)


# --- Chat Display --- #
chat_area = st.container()
with chat_area:
	if not st.session_state.lc_messages:
		st.info(
			"Start a conversation to engage the agent. Context and guardrails adapt to your inputs."
		)
	for msg in st.session_state.lc_messages:
		role = "assistant" if isinstance(msg, AIMessage) else "user"
		content = msg.content if isinstance(msg.content, str) else str(msg.content)
		with st.chat_message(role):
			st.markdown(content)


# --- Helper: Build Context --- #
def build_context() -> SentinelContext:
	return SentinelContext(
		user_id=user_id,
		user_name=user_name,
		department=department,
		clearance_level=clearance_level,  # Keep as integer; schema type is flexible
		tenant_id=tenant_id,
		deployment_env=deployment_env,
		session_id=st.session_state.session_id,
		request_id=str(uuid.uuid4()),
		is_audit_enabled=is_audit_enabled,
		compliance_frameworks=compliance_frameworks,
	)


# --- Interaction --- #
user_prompt = st.chat_input("Send a message to SentinelNexus")

if user_prompt:
	if "api_key" not in st.session_state:
		st.warning("Please provide an OpenAI API key in the sidebar to run the agent.")
	else:
		st.session_state.lc_messages.append(HumanMessage(content=user_prompt))

		# Ensure agent is initialized only when key is available
		base_agent = get_sentinel_agent()

		context = build_context()
		
		payload = {
			"messages": st.session_state.lc_messages,
		}
		config = {
			"configurable": {
				"thread_id": st.session_state.session_id,
			}
		}

		with st.spinner("Routing through middleware and tools..."):
			try:
				# Stream the agent execution to properly handle tool calls
				result_messages = list(st.session_state.lc_messages)
				
				for output in base_agent.stream(payload, config=config, context=context):
					# LangGraph stream output is structured as {node_name: {state}}
					# Extract messages from any node output
					for node_name, node_output in output.items():
						if isinstance(node_output, dict) and "messages" in node_output:
							result_messages = node_output["messages"]
				
				st.session_state.lc_messages = result_messages
				
			except Exception as exc:  # noqa: BLE001
				st.session_state.lc_messages.append(
					AIMessage(content=f"Agent run failed: {str(exc)[:500]}")
				)

		st.rerun()


# --- Footer Notes --- #
with st.expander("Operational Notes", expanded=False):
	st.markdown(
		"- API keys are held in Streamlit session_state and cleared on refresh/close."
		"\n- No backend code is modified; the app only orchestrates the existing agent."
		"\n- Use the reset control to flush chat, state, and keys immediately."
	)
