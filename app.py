import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, List, Any

# Page configuration
st.set_page_config(
    page_title="Literary Analysis Agent",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
        font-size: 16px;
    }
    .chat-message {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        gap: 10px;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2E86AB;
        color: #000;
    }
    .assistant-message {
        background-color: #E8D5F2;
        border-left: 4px solid #7B2CBF;
        color: #1a1a1a;
    }
    .sidebar-info {
        padding: 15px;
        background-color: #E3F2FD;
        border-radius: 8px;
        margin-bottom: 20px;
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("### Configuration")
    
    # API Key Input
    api_key = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        help="Your API key is not stored and only used for this session"
    )
    
    st.divider()
    
    # Domain input
    st.markdown("### Literary Work Settings")
    literary_work = st.text_input(
        "Enter the literary work to focus on:",
        placeholder="e.g., 'Pride and Prejudice', 'Hamlet', '1984'",
        help="The agent will focus analysis on this specific work"
    )
    
    st.divider()
    
    # Model settings
    st.markdown("### Model Settings")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1,
        help="Lower values = more deterministic, Higher values = more creative"
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100,
        help="Maximum length of the response"
    )
    
    st.divider()
    
    st.markdown("""
    <div class="sidebar-info">
        <strong>About this Agent</strong><br>
        This is a Literary Analysis Assistant that provides focused analysis on a specific literary work. 
        It will refuse to answer questions outside the selected domain.
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown("<h1 class='main-header'>Literary Analysis Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Intelligent literary analysis powered by LangChain & OpenAI</p>", unsafe_allow_html=True)

# Check if API key is provided
if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to get started.")
    st.stop()

if not literary_work:
    st.warning("Please enter the literary work you'd like to analyze in the sidebar.")
    st.stop()

# Set environment variable for API key
os.environ["OPENAI_API_KEY"] = api_key

# Define the domain enforcement logic
def check_domain_relevance(user_input: str, literary_work: str) -> bool:
    """Check if user input is related to the literary work"""
    return literary_work.lower() in user_input.lower()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = None
    st.session_state.last_api_key = None
    st.session_state.last_literary_work = None

# Recreate model if API key, work, or settings changed
if (api_key != st.session_state.last_api_key or 
    literary_work != st.session_state.last_literary_work):
    
    system_prompt_content = (
        f"You are a literary analysis assistant specializing in {literary_work}.\n"
        f"Your task is to analyze and explain concepts strictly related to {literary_work}.\n"
        "Respond concisely, with clear literary reasoning.\n"
        "Do not speculate beyond the provided work or discuss other literary works.\n"
        "Always provide specific examples and textual references when possible."
    )

    st.session_state.model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=30
    )
    
    st.session_state.system_prompt = system_prompt_content
    st.session_state.last_api_key = api_key
    st.session_state.last_literary_work = literary_work
    st.session_state.messages = []  # Clear chat history on model recreation

# Display chat history
st.markdown("### Conversation")
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            st.markdown(
                f"""<div class="chat-message user-message">
                <div><strong>You:</strong> {message.content}</div>
                </div>""",
                unsafe_allow_html=True
            )
        elif isinstance(message, AIMessage):
            st.markdown(
                f"""<div class="chat-message assistant-message">
                <div><strong>Agent:</strong> {message.content}</div>
                </div>""",
                unsafe_allow_html=True
            )

# Input area
st.markdown("### Ask a Question")
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Your question about the literary work:",
        placeholder=f"Ask something about {literary_work}...",
        label_visibility="collapsed"
    )

with col2:
    submit_button = st.button("Send", type="primary", use_container_width=True)

# Process user input
if submit_button and user_input:
    # Check if input is relevant to the literary work
    if not check_domain_relevance(user_input, literary_work):
        st.error("Please ask something related to literary_work.")
    else:
        # Add user message to history
        st.session_state.messages.append(HumanMessage(content=user_input))
        
        # Display loading indicator
        with st.spinner("Analyzing..."):
            try:
                # Build messages for the model
                messages_for_model = [
                    {"role": "system", "content": st.session_state.system_prompt}
                ]
                
                # Add chat history
                for msg in st.session_state.messages:
                    if isinstance(msg, HumanMessage):
                        messages_for_model.append({"role": "user", "content": msg.content})
                    elif isinstance(msg, AIMessage):
                        messages_for_model.append({"role": "assistant", "content": msg.content})
                
                # Get response from model
                response = st.session_state.model.invoke(messages_for_model)
                
                # Extract assistant response
                assistant_message = response.content
                
                # Add assistant message to history
                st.session_state.messages.append(AIMessage(content=assistant_message))
                
                # Rerun to display new messages
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.pop()  # Remove the user message if there was an error

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px; margin-top: 20px;'>
    <p>Built with Streamlit & LangChain | Powered by OpenAI GPT-4o-mini</p>
</div>
""", unsafe_allow_html=True)
