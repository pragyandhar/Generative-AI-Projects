# 📚 Literary Analysis Agent - Strict Scope LangChain Agent

A deterministic, domain-locked LangChain agent that specializes in analyzing specific literary works. Built with Streamlit for an elegant user interface.

## 🎯 Features

- **Domain-Locked Analysis**: Agent strictly focuses on a single literary work and refuses to answer questions outside that domain
- **Middleware Enforcement**: Custom middleware ensures strict scope control
- **Beautiful UI**: Modern Streamlit interface with intuitive controls
- **API Key Management**: Input your OpenAI API key directly in the app (not stored)
- **Configurable Settings**: Adjust temperature and max tokens for different response styles
- **Chat History**: Maintains conversation history within each session
- **Literary Reasoning**: Provides concise, evidence-based literary analysis

## Live Working Demonstration
https://scrict-scope-agent.streamlit.app/

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Generative-AI-Projects
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Launch the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter OpenAI API Key**: Paste your OpenAI API key in the sidebar (it's not stored)
2. **Select Literary Work**: Enter the literary work you want to analyze (e.g., "Pride and Prejudice", "Hamlet", "1984")
3. **Adjust Settings** (optional): Configure temperature and max tokens
4. **Ask Questions**: Type your literary analysis questions and get focused responses

## 🏗️ Project Structure

- `main.py` - Core agent implementation with custom state and middleware
- `app.py` - Streamlit application with UI
- `requirements.txt` - Python dependencies

## 🔧 Technical Details

### Custom Components

- **LiteraryState**: Extended AgentState with `allowed_domain` field
- **DomainEnforcementMiddleware**: Middleware that validates user queries against the allowed domain
- **SystemPrompt**: Configurable system message that defines agent behavior

### Model Configuration

- **Model**: GPT-4o-mini (cost-effective, fast)
- **Temperature**: 0.1 (default, deterministic)
- **Max Tokens**: 1000 (default, adjustable)

## 🎨 UI Features

- Clean, modern design with color-coded messages
- Responsive layout with sidebar configuration
- Loading indicator during processing
- Error handling and user feedback
- Information panels with helpful tips

## 📝 Example Usage

```
User: "What are the main themes in Pride and Prejudice?"
Agent: [Provides focused analysis on Pride and Prejudice themes]

User: "Tell me about Game of Thrones"
Agent: [Politely refuses and redirects to the selected work]
```

## ⚙️ Environment Variables

The app requires:
- `OPENAI_API_KEY`: Your OpenAI API key (input in the app sidebar)

## 📄 License

This project is part of the Generative AI learning journey.
