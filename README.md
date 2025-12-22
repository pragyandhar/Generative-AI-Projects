# Celebrity Search Application

A simple Streamlit app that uses LangChain + OpenAI to fetch a short celebrity bio, extract the birth year, and list five notable global historical events from that year.

**Features**
- **Bio summary:** 3-line engaging overview for a given celebrity.
- **Birth year extraction:** Derives the year from the provided celebrity name.
- **Historical events:** Returns 5 significant worldwide events for that birth year.
- **Clean UI:** Spinner while fetching, expandable sections for each result.
- **LangChain-powered:** Uses `ChatOpenAI`, `ChatPromptTemplate`, and `StrOutputParser`.

**Tech Stack**
- **Framework:** Streamlit
- **LLM Orchestration:** LangChain
- **Model Provider:** OpenAI (`gpt-4o-mini`)

**Prerequisites**
- **Python:** 3.10+ recommended
- **OpenAI API key:** Active key with access to `gpt-4o-mini` or compatible models

**Setup**
1. Create and activate a virtual environment.
	 ```bash
	 python -m venv .venv
	 source .venv/bin/activate
	 ```
2. Install dependencies.
	 ```bash
	 pip install -r requirements.txt
	 ```
3. Provide your OpenAI API key.
	 - Preferred: create a `.env` file in the project root with:
		 ```env
		 OPENAI_API=sk-your-openai-key
		 ```
	 - Alternatively, export it in your shell:
		 ```bash
		 export OPENAI_API=sk-your-openai-key
		 ```
	 Notes:
	 - The app calls `load_dotenv()` and reads `OPENAI_API`, then sets `OPENAI_API_KEY` internally.
	 - If you already use `OPENAI_API_KEY`, you can also export that directly.

**Run**
```bash
streamlit run main.py
```

**Usage**
- Enter a celebrity name (e.g., "Elon Musk").
- The app shows:
	- A short biography
	- The inferred birth year
	- Five important global historical facts from that year

**How It Works**
- Prompts and chains in [main.py](main.py):
	- **`chain_about`**: `"Write a 3-line engaging short and concise summary about the celebrity {name}"`
	- **`chain_dob`**: `"Based on the given description, give me the birth year of the following celebrity {name}"`
	- **`chain_history`**: `"From the above birth year {birth_year}, give me 5 important historical facts which happened all across the world"`
- Each chain is built with `ChatPromptTemplate | ChatOpenAI | StrOutputParser` and executed sequentially.

**Configuration**
- Model: set in [main.py](main.py) within `ChatOpenAI(model='gpt-4o-mini', ...)`.
- Temperature: default `0.8` (more creative). Lower for more precise outputs.
- Max completion tokens: `1000`.
- Timeout: `300` seconds.

**Troubleshooting**
- **Missing API key:** Ensure `.env` contains `OPENAI_API` or your shell exports it. Restart the app after setting.
- **Model access errors:** Switch to an available model in [main.py](main.py) if your account lacks `gpt-4o-mini` access.
- **Rate limits / 429:** Reduce usage or add retries; try again later.
- **Network issues:** Verify internet connectivity from the container/host.

**Limitations**
- Outputs may contain inaccuracies or hallucinations; verify facts.
- Ambiguous names or lesser-known celebrities may reduce accuracy.
- Historical events are generated text, not guaranteed to be authoritative.

**Privacy**
- Input prompts and context are sent to OpenAI to generate responses.
- Avoid entering sensitive personal data.

**Project Files**
- [main.py](main.py): Streamlit app and LangChain chains.
- [requirements.txt](requirements.txt): Python dependencies.
- `.env` (create this): Stores `OPENAI_API`.

Made by Pragyan Dhar
