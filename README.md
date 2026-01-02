# AI Auto Tutor

A LangChain-powered educational AI system that generates structured lessons, quizzes, and provides detailed token-level analytics for learning any topic.

## Project Overview

This project demonstrates advanced usage of LangChain with OpenAI's GPT-4o-mini model to create an intelligent tutoring system. The system breaks down complex topics into manageable steps, provides real-world examples, generates progressive quizzes, and offers detailed metrics about model behavior.

## Core Features

- **Structured Lesson Generation**: Converts raw AI responses into organized lessons with steps, examples, and quizzes
- **Quiz Generation**: Automatically creates 5 progressively difficult questions on any topic
- **Token & Logprob Analytics**: Detailed metrics on input/output tokens, response time, and token-level probabilities
- **Math Expression Solving**: Solves mathematical equations using symbolic computation
- **Wikipedia Integration**: Attaches relevant Wikipedia summaries as context
- **Redis Caching**: Caches responses with configuration-aware keys to prevent redundant API calls
- **Streaming Output**: Real-time token-by-token response display for better UX

## File Structure

### Core Backend (Original Files)

**model.py** - Main orchestration file (authored by user)
- Builds the LangChain chain with prompt template and bound tools
- Implements three invocation modes: basic, structured, and streaming
- Manages Redis caching with context-aware cache keys
- Configurable temperature and max tokens

**structured.py** - Structured lesson extraction
- Pydantic schema for lesson output (topic, steps, examples, quiz)
- Uses LangChain's structured output binding for consistent formatting

**quiz_generator.py** - Quiz creation tool
- LangChain tool decorator for integration with agent chains
- Generates 5 numbered questions in increasing difficulty order

**math_solver.py** - Math expression evaluator
- Uses SymPy to solve algebraic equations
- Integrates as a LangChain tool for agent use

**wikipedia.py** - Wikipedia lookup tool
- LangChain tool for fetching concise summaries
- Provides context for questions about named entities and topics

**analytics.py** - Token and probability metrics
- Calls OpenAI API with logprobs enabled
- Returns token usage, response time, and top-3 token alternatives

### Streamlit Frontend (Demonstration by AI)

**app_streamlit.py** - Interactive web interface (authored as demonstration)
- Session-based API key input (no persistence)
- Rich sidebar controls for tone, audience, format, quiz difficulty
- Multi-select extra directives (analogies, pitfalls, mnemonics, exercises)
- Optional math and Wikipedia context attachment
- Three-tab interface: Tutor Answer, Structured Lesson, Token Metrics
- Session history tracking with recent runs display
- Download button for generated answers
- Raw JSON export of structured lessons

## Requirements

```
langchain
langchain-openai
streamlit
pydantic
sympy
wikipedia
redis
openai
```

## Installation & Setup

1. Clone the repository and navigate to the project directory

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Redis is running:
   ```bash
   redis-server
   ```

4. Set your OpenAI API key (optional for Streamlit, but required for direct Python usage):
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## Usage

### Direct Python Usage

```python
from model import basic_invocation, structured_response, streaming_response

api_key = "your-openai-key"
question = "Explain photosynthesis"

# Plain text response with caching
answer = basic_invocation(question, api_key)

# Structured response with steps and quiz
lesson = structured_response(question, api_key)

# Streaming response
stream_answer = streaming_response(question, api_key)
```

### Streamlit Web Interface

Run the Streamlit app:
```bash
streamlit run app_streamlit.py
```

Then:
1. Enter your OpenAI API key in the sidebar (session-only)
2. Adjust tone, audience, format, and quiz difficulty
3. Select optional directives (analogies, pitfalls, etc.)
4. Toggle Wikipedia/math context if needed
5. Enter your question and click "Run Tutor"
6. View tutor answer, structured lesson, and token metrics in tabs

## Architecture Details

### Cache Key Design

The cache key combines:
- Model name (gpt-4o-mini)
- Temperature setting
- Hash of the system prompt
- List of attached tools
- User question

This ensures that changing any configuration invalidates old cache entries, preventing stale responses.

### Response Pipeline

1. User submits a question with style constraints
2. If cached, return immediately
3. Otherwise, invoke LangChain chain with prompt + tools
4. Optionally stream tokens in real-time
5. Cache result for 1 hour
6. User can then generate structured lesson and token metrics on demand

### Structured Output

Using Pydantic + LangChain's `with_structured_output`, responses are coerced into the Lesson schema:
- Topic (single string)
- Steps (list of concise step descriptions)
- Examples (list of real-world examples)
- Quiz (list of 5 progressively difficult questions)

## Configuration

### Temperature
Range: 0.0 (deterministic) to 1.0 (creative)
Default: 0.5
Effects: Lower for factual answers, higher for brainstorming

### Max Completion Tokens
Range: 64 to 2000
Default: 800
Adjusts max response length

### Style Controls (Streamlit)
- **Tone**: Concise, Supportive, Technical, Exam-focused
- **Audience**: Middle school, High school, Undergrad, Professional
- **Format**: Bulleted steps, Short paragraphs, Mixed
- **Quiz Difficulty**: 1 (easiest) to 5 (hardest)
- **Extras**: Analogies, Common pitfalls, Mnemonics, Practice exercises

## Session History

The Streamlit app maintains an in-memory session history showing:
- Question preview (first 40 characters)
- Timestamp of the run
- Quiz level used
- Temperature setting

History is not persisted to disk and is cleared on app restart.

## Error Handling

- Missing API key: User is prompted to enter it in the sidebar
- Redis unavailable: RuntimeError raised; ensure Redis is running
- Invalid math expression: Tool returns error message instead of crashing
- Wikipedia lookup failure: Returns "No result found"

## Performance Notes

- First run for a question: ~2-5 seconds (depending on network)
- Cached run: Instant (Redis retrieval)
- Structured lesson generation: ~3-7 seconds (second LLM call)
- Token metrics: ~2-3 seconds (includes logprobs computation)

## Limitations

- OpenAI API calls incur costs per token
- Redis caching only works for identical questions and settings
- Streaming is disabled when cached results are retrieved
- Structured output may sometimes reformat quiz questions

## Future Enhancements

- Persistent user sessions and run history
- Support for multiple LLM backends (Claude, Gemini, local models)
- Customizable system prompts via UI
- Quiz answer grading and feedback
- Export to PDF or Markdown
- Interactive quiz mode with real-time scoring
- Multi-language support

## Attribution

- **Backend Core (model.py, structured.py, quiz_generator.py, math_solver.py, wikipedia.py, analytics.py)**: Developed by the user as part of the LangChain mastery project
- **Streamlit Frontend (app_streamlit.py)**: Developed by AI for demonstration purposes only, showcasing how the backend can be integrated into an interactive web interface
- **LangChain Integration**: Demonstrates best practices for prompt composition, tool binding, and structured outputs
- **Redis Caching Strategy**: Implements context-aware cache keys to prevent configuration mismatches

## License

This project is part of the Generative-AI-Projects repository and follows the repository's license terms.

## Support

For issues or questions about the backend core, refer to the original model files and their docstrings. For Streamlit UI feedback, this is a demonstration layer and can be freely modified for your use case.
