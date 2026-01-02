# Smart Agent Playground - A Full-Stack LLM Model App Using LangChain

A comprehensive learning project demonstrating various LangChain capabilities with OpenAI's GPT-4o-mini model. This repository contains hands-on implementations of core LangChain patterns including basic invocation, streaming, tool usage, structured outputs, and model analytics.

## Project Overview

This project serves as a practical exploration of LangChain for Generative AI development. It showcases different interaction patterns with Large Language Models (LLMs) through both a FastAPI backend and an interactive Streamlit frontend.

## Features

### 1. Basic LLM Invocation
Simple question-answering with the LLM using LangChain's ChatOpenAI interface.

### 2. Streaming Responses
Real-time text generation demonstrating streaming capabilities for improved user experience.

### 3. Weather Agent with Tools
Implementation of an AI agent with tool-calling capabilities:
- Uses LangChain's `@tool` decorator
- Integrates with Visual Crossing Weather API
- Demonstrates agent reasoning and tool execution workflow

### 4. Structured Output
Enforces JSON schema using Pydantic models:
- Generates summaries with predefined structure
- Returns title, key points, and confidence scores
- Demonstrates `with_structured_output` pattern

### 5. Log Probabilities Analysis
Token-level confidence scoring using OpenAI's logprobs feature for understanding model certainty.

## Tech Stack

- **Framework**: FastAPI, Streamlit
- **LLM Integration**: LangChain, LangChain-OpenAI
- **LLM Provider**: OpenAI (GPT-4o-mini)
- **Validation**: Pydantic v2
- **External APIs**: Visual Crossing Weather API
- **Python**: 3.12+

## Live Working Demonstration Link
https://smart-agent-playground.streamlit.app/

## Project Structure

```
.
├── app.py                  # FastAPI backend with REST endpoints
├── models.py              # Basic LLM invocation and streaming
├── tools.py               # Weather agent with tool calling
├── structured.py          # Structured output with Pydantic
├── analytics.py           # Token log probabilities analysis
├── cache.py               # LRU caching utility
├── proxy.py               # Custom base URL configuration
├── streamlit_app.py       # Interactive Streamlit frontend (AI-generated)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
└── README.md             # This file
```

## File Attribution

**Note**: All core functionality files (`app.py`, `models.py`, `tools.py`, `structured.py`, `analytics.py`, `cache.py`, `proxy.py`) were written manually as part of the learning process. Only `streamlit_app.py` was generated using AI assistance to provide an interactive frontend interface.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pragyandhar/Generative-AI-Projects.git
cd Generative-AI-Projects
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

## Usage

### Option 1: Streamlit App (Recommended)

Run the interactive Streamlit application:
```bash
streamlit run streamlit_app.py
```

The app will open in your browser where you can:
- Enter your API keys securely in the sidebar
- Test all features through an intuitive interface
- See real-time streaming responses
- Analyze structured outputs and log probabilities

### Option 2: FastAPI Backend

Run the FastAPI server:
```bash
uvicorn app:app --reload
```

Access the API endpoints:
- `GET /invoke?q=your_question` - Basic invocation
- `GET /stream?q=your_question` - Streaming response
- `GET /weather?q=weather_query` - Weather agent
- `GET /summary?q=text_to_summarize` - Structured summary
- `GET /logprobs?q=your_prompt` - Log probabilities

API documentation available at: `http://localhost:8000/docs`

## API Endpoints

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/invoke` | Simple LLM response | `/invoke?q=What is LangChain?` |
| `/stream` | Streaming response | `/stream?q=Tell me a story` |
| `/weather` | Weather agent with tools | `/weather?q=Weather in London?` |
| `/summary` | Structured JSON summary | `/summary?q=Long text here...` |
| `/logprobs` | Token probabilities | `/logprobs?q=The capital of France is` |

## Key Learning Concepts

### LangChain Patterns Demonstrated

1. **Lazy Initialization**: Models are created only when needed, allowing for runtime API key configuration
2. **Tool Binding**: Agents can call external tools using `bind_tools()`
3. **Structured Output**: Schema enforcement using Pydantic with `with_structured_output()`
4. **Streaming**: Generator-based streaming for real-time responses
5. **Message Handling**: Proper use of `HumanMessage` and message history

### Design Patterns

- **Separation of Concerns**: Each module handles a specific LangChain pattern
- **Environment-based Configuration**: API keys stored securely in environment variables
- **Error Handling**: Graceful error handling across all endpoints
- **Session-based Security**: Streamlit app uses session-only API key storage

## Security Notes

- Never commit your `.env` file to version control
- API keys in the Streamlit app are stored only in the session and never persisted to disk
- Always use environment variables for sensitive credentials

## Learning Path

This project demonstrates progressive learning of LangChain:
1. Start with basic invocation (`models.py`)
2. Add streaming capabilities
3. Implement agents with tools (`tools.py`)
4. Enforce structured outputs (`structured.py`)
5. Analyze model behavior (`analytics.py`)

## Future Enhancements

Potential additions for continued learning:
- Memory and conversation history
- RAG (Retrieval Augmented Generation)
- Multiple agent collaboration
- Custom chains and LCEL
- Vector database integration
- Advanced prompt engineering

## Dependencies

Key dependencies include:
- `langchain>=1.0` - Core LangChain functionality
- `langchain-openai` - OpenAI integration
- `openai` - OpenAI API client
- `fastapi` - REST API framework
- `streamlit` - Interactive web interface
- `pydantic>=2,<3` - Data validation
- `uvicorn` - ASGI server

See `requirements.txt` for complete list.

## Contributing

This is a personal learning repository. Feel free to fork and experiment with your own LangChain implementations.

## License

This project is for educational purposes. Refer to individual API provider terms of service (OpenAI, Visual Crossing) for usage restrictions.

## Acknowledgments

- LangChain documentation and community
- OpenAI for GPT-4o-mini access
- Visual Crossing for weather API
- Streamlit for the frontend framework

## Author

**Pragyandhar**

Branch: `P3-Smart-Agent-Playground---A-Full-Stack-LLM-Model-App-Using-LangChain`

---

*This README documents a learning project for mastering LangChain and Generative AI development.*
