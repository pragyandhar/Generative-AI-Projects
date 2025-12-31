import streamlit as st
from models import invoke_model, stream_model
from tools import weather_agent
from structured import structured_summary
from analytics import get_logprobs
import os

# Page configuration
st.set_page_config(
    page_title="Smart Agent Playground",
    layout="wide"
)

# Title and description
st.title("Smart Agent Playground")
st.markdown("**A Full-Stack LLM Model App Using LangChain**")
st.markdown("---")

# Sidebar for API keys
with st.sidebar:
    st.header("API Configuration")
    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key. It will only be stored in this session."
    )
    
    weather_key = st.text_input(
        "Weather API Key (Optional)",
        type="password",
        help="Enter your Visual Crossing Weather API key for weather agent."
    )
    
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("""
    - **Basic Invoke**: Simple LLM responses
    - **Streaming**: Real-time text generation
    - **Weather Agent**: Tool-calling with agents
    - **Structured Output**: JSON schema enforcement
    - **Log Probabilities**: Token confidence analysis
    """)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app demonstrates various LangChain capabilities with GPT-4o-mini.")

# Check if API key is provided
if not openai_key:
    st.warning("Please enter your OpenAI API key in the sidebar to get started.")
    st.info("Your API key is only stored in this session and never saved permanently.")
    st.stop()

# Set API keys in environment (session-based)
os.environ["OPENAI_API_KEY"] = openai_key
if weather_key:
    os.environ["WEATHER_API_KEY"] = weather_key

# Create tabs for different functionalities
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Basic Invoke",
    "Streaming",
    "Weather Agent",
    "Structured Output",
    "Log Probabilities"
])

# Tab 1: Basic Invoke
with tab1:
    st.header("Basic LLM Invocation")
    st.markdown("Get a simple response from the LLM.")
    
    prompt1 = st.text_area(
        "Enter your prompt:",
        placeholder="Ask me anything...",
        height=100,
        key="invoke_prompt"
    )
    
    if st.button("Invoke Model", key="invoke_btn"):
        if prompt1:
            with st.spinner("Generating response..."):
                try:
                    result = invoke_model(prompt1)
                    st.success("Response generated!")
                    st.markdown("### Response:")
                    st.write(result["text"])
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a prompt.")

# Tab 2: Streaming
with tab2:
    st.header("Streaming Responses")
    st.markdown("See the LLM generate text in real-time.")
    
    prompt2 = st.text_area(
        "Enter your prompt:",
        placeholder="Tell me a story...",
        height=100,
        key="stream_prompt"
    )
    
    if st.button("Stream Response", key="stream_btn"):
        if prompt2:
            st.markdown("### Streamed Response:")
            try:
                st.write_stream(stream_model(prompt2))
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a prompt.")

# Tab 3: Weather Agent
with tab3:
    st.header("Weather Agent with Tools")
    st.markdown("Ask about the weather using an AI agent with tool-calling capabilities.")
    
    if not weather_key:
        st.warning("Weather API key not configured. Enter it in the sidebar to use this feature.")
    
    prompt3 = st.text_input(
        "Ask about the weather:",
        placeholder="What's the weather like in London?",
        key="weather_prompt"
    )
    
    if st.button("Run Weather Agent", key="weather_btn"):
        if prompt3:
            with st.spinner("Agent is thinking and using tools..."):
                try:
                    result = weather_agent(prompt3)
                    st.success("Agent completed!")
                    st.markdown("### Agent Response:")
                    st.write(result["response"])
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a question.")

# Tab 4: Structured Output
with tab4:
    st.header("Structured Output")
    st.markdown("Get structured JSON output with Pydantic schema enforcement.")
    
    prompt4 = st.text_area(
        "Enter text to summarize:",
        placeholder="Enter a long text that you want to summarize...",
        height=150,
        key="summary_prompt"
    )
    
    if st.button("Generate Summary", key="summary_btn"):
        if prompt4:
            with st.spinner("Generating structured summary..."):
                try:
                    result = structured_summary(prompt4)
                    st.success("Summary generated!")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("### Summary")
                        st.subheader(result["title"])
                        st.markdown("**Key Points:**")
                        for i, point in enumerate(result["key_points"], 1):
                            st.markdown(f"{i}. {point}")
                    
                    with col2:
                        st.markdown("### Confidence Score")
                        st.metric("Score", f"{result['score']:.2f}")
                        
                    st.markdown("---")
                    st.json(result)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter text to summarize.")

# Tab 5: Log Probabilities
with tab5:
    st.header("Token Log Probabilities")
    st.markdown("Analyze token-level confidence scores from the model.")
    
    prompt5 = st.text_input(
        "Enter a prompt:",
        placeholder="The capital of France is",
        key="logprob_prompt"
    )
    
    if st.button("Analyze Probabilities", key="logprob_btn"):
        if prompt5:
            with st.spinner("Analyzing token probabilities..."):
                try:
                    result = get_logprobs(prompt5)
                    st.success("Analysis complete!")
                    
                    st.markdown("### Generated Content:")
                    st.write(result["content"])
                    
                    st.markdown("### Log Probabilities:")
                    st.json(result["logprobs"])
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a prompt.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ using LangChain, OpenAI, and Streamlit</p>
        <p style='font-size: 0.8em; color: gray;'>
            Your API keys are only stored in this session and are never saved to disk.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
