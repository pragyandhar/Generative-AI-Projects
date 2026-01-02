import os
import time
import streamlit as st
from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from openai import OpenAI

from math_solver import solve_math
from wikipedia import wikipedia_lookup

st.set_page_config(page_title="AI Auto Tutor", layout="wide")

# lightweight styling to create stronger section separation
st.markdown(
    """
    <style>
    .section-card {padding: 1rem 1.25rem; border: 1px solid #E6E8EB; border-radius: 10px; background: #F9FAFB;}
    .pill {padding: 0.15rem 0.7rem; border-radius: 999px; border: 1px solid #D0D7DE; font-size: 0.8rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Prompt used for the main tutor answer
TUTOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert AI Tutor. Answer succinctly, break the concept into short, numbered steps,
            provide one real-life example, and end with 5 quiz questions that increase in difficulty.
            Keep wording tight and avoid fluff.
            """,
        ),
        ("human", "{question}"),
    ]
)

# Schema for structured lesson output
class Lesson(BaseModel):
    topic: str
    steps: List[str]
    examples: List[str]
    quiz: List[str]


def ensure_api_key() -> Optional[str]:
    """Retrieve API key from session, mirror to env for downstream libs."""
    key = st.session_state.get("api_key", "").strip()
    if key:
        os.environ["OPENAI_API_KEY"] = key
        return key
    return None


def build_llm(api_key: str, temperature: float, max_tokens: int) -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key,
        temperature=temperature,
        max_completion_tokens=max_tokens,
    )


def run_tutor(question: str, api_key: str, temperature: float, max_tokens: int, stream: bool) -> str:
    llm = build_llm(api_key, temperature, max_tokens)
    chain = TUTOR_PROMPT | llm

    if not stream:
        result = chain.invoke({"question": question})
        return result.content

    text_placeholder = st.empty()
    full = ""
    for chunk in chain.stream({"question": question}):
        full += chunk.content
        text_placeholder.markdown(full)
    return full


def get_structured_lesson(question: str, api_key: str, temperature: float, max_tokens: int) -> Lesson:
    llm = build_llm(api_key, temperature, max_tokens)
    structured = llm.with_structured_output(Lesson)
    result = structured.invoke([{"role": "user", "content": f"Create a concise lesson on: {question}"}])
    return result


def token_metrics(prompt: str, api_key: str):
    client = OpenAI(api_key=api_key)
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        logprobs=True,
        top_logprobs=3,
    )
    duration = time.time() - start
    usage = resp.usage
    first_token = resp.choices[0].logprobs.content[:1] if resp.choices[0].logprobs else []
    return {
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "duration_seconds": round(duration, 3),
        "first_token_logprobs": first_token,
        "text": resp.choices[0].message.content,
    }


def main():
    if "history" not in st.session_state:
        st.session_state["history"] = []

    st.title("AI Auto Tutor")
    st.caption("Session-only key. Learn quickly with steps, examples, and quizzes.")

    with st.sidebar:
        st.header("Session Setup")
        key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            help="Key is kept only in this session and not stored.",
        )
        if key_input:
            st.session_state["api_key"] = key_input
            ensure_api_key()

        temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.05)
        max_tokens = st.slider("Max completion tokens", 64, 2000, 800, 32)
        stream = st.toggle("Stream output", value=True)
        style_tone = st.selectbox("Tone", ["Concise", "Supportive", "Technical", "Exam-focused"], index=1)
        style_audience = st.selectbox("Audience", ["Middle school", "High school", "Undergrad", "Professional"], index=2)
        style_format = st.selectbox("Answer format", ["Bulleted steps", "Short paragraphs", "Mixed"], index=0)
        quiz_level = st.slider("Quiz difficulty (1 easiest, 5 hardest)", 1, 5, 3)
        extras = st.multiselect(
            "Extra directives",
            [
                "Add analogies",
                "Call out common pitfalls",
                "Include a quick mnemonic",
                "Suggest a practice exercise",
            ],
            default=["Call out common pitfalls"],
        )
        with st.expander("Add context"):
            use_wiki = st.checkbox("Attach Wikipedia summary", value=False)
            use_math = st.checkbox("Solve as math expression", value=False)

        if st.session_state["history"]:
            st.markdown("### Recent Runs")
            for item in st.session_state["history"][-5:][::-1]:
                st.markdown(
                    f"- **{item['question'][:40]}...** — {item['timestamp']} | Quiz {item.get('quiz_level', 3)} | Temp {item.get('temperature', 0.5)}"
                )

    question = st.text_area(
        "Ask the tutor",
        value="Explain gravity in simple terms",
        height=140,
    )


    col_run, col_clear = st.columns([3, 1])
    with col_run:
        run_clicked = st.button("Run Tutor", type="primary")
    with col_clear:
        if st.button("Clear"):
            st.session_state.pop("last_answer", None)
            st.session_state.pop("last_question", None)

    if run_clicked:
        api_key = ensure_api_key()
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
            st.stop()

        context_parts = []
        math_text = None
        wiki_text = None
        if use_math:
            math_text = solve_math.run(question)
            context_parts.append(f"Math solver output: {math_text}")
        if use_wiki:
            wiki_text = wikipedia_lookup.run(question)
            context_parts.append(f"Wikipedia summary: {wiki_text}")

        final_question = question
        if context_parts:
            final_question = question + "\n\n" + "\n".join(context_parts)

        style_lines = [
            f"Tone: {style_tone}",
            f"Audience: {style_audience}",
            f"Format: {style_format}",
            f"Quiz difficulty target: {quiz_level} (5 = hardest)",
        ]
        if extras:
            style_lines.append("Extras: " + "; ".join(extras))
        final_question = final_question + "\n\nStyle and constraints:\n" + "\n".join(f"- {line}" for line in style_lines)

        with st.spinner("Thinking..."):
            answer = run_tutor(
                question=final_question,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )

        st.session_state["last_answer"] = answer
        st.session_state["last_question"] = question
        st.session_state["last_context"] = {
            "math": math_text,
            "wiki": wiki_text,
            "use_math": use_math,
            "use_wiki": use_wiki,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "style_tone": style_tone,
            "style_audience": style_audience,
            "style_format": style_format,
            "quiz_level": quiz_level,
            "extras": extras,
        }

        st.session_state["history"].append(
            {
                "question": question,
                "timestamp": time.strftime("%H:%M:%S"),
                "stream": stream,
                "temperature": temperature,
                "quiz_level": quiz_level,
            }
        )

    if "last_answer" in st.session_state:
        # quick status grid
        ctx = st.session_state.get("last_context", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Temperature", ctx.get("temperature", 0.5))
        c2.metric("Max tokens", ctx.get("max_tokens", 800))
        c3.metric("Streaming", "On" if ctx.get("stream", True) else "Off")
        c4.metric("Quiz level", ctx.get("quiz_level", 3))

        tabs = st.tabs(["Tutor Answer", "Structured Lesson", "Token Metrics"])

        with tabs[0]:
            st.markdown(st.session_state["last_answer"])
            ctx = st.session_state.get("last_context", {})
            if ctx.get("use_math") and ctx.get("math"):
                st.info(f"Math solver: {ctx['math']}")
            if ctx.get("use_wiki") and ctx.get("wiki"):
                st.info(f"Wikipedia: {ctx['wiki']}")

            st.download_button(
                "Download answer",
                data=st.session_state["last_answer"],
                file_name="tutor_answer.txt",
            )

        with tabs[1]:
            api_key = ensure_api_key()
            if not api_key:
                st.warning("Enter API key to generate structured lesson.")
            else:
                ctx = st.session_state.get("last_context", {})
                with st.spinner("Structuring lesson..."):
                    lesson = get_structured_lesson(
                        st.session_state["last_question"],
                        api_key=api_key,
                        temperature=ctx.get("temperature", 0.5),
                        max_tokens=ctx.get("max_tokens", 800),
                    )
                st.subheader(lesson.topic)
                st.markdown("**Steps**")
                for step in lesson.steps:
                    st.markdown(f"- {step}")
                st.markdown("**Example**")
                for ex in lesson.examples:
                    st.markdown(f"- {ex}")
                st.markdown("**Quiz**")
                for q in lesson.quiz:
                    st.markdown(f"- {q}")

                with st.expander("Raw lesson JSON"):
                    st.json(lesson.dict())

        with tabs[2]:
            api_key = ensure_api_key()
            if not api_key:
                st.warning("Enter API key to compute token metrics.")
            else:
                with st.spinner("Fetching metrics..."):
                    metrics = token_metrics(st.session_state["last_question"], api_key=api_key)
                st.write(
                    {
                        "input_tokens": metrics["input_tokens"],
                        "output_tokens": metrics["output_tokens"],
                        "total_tokens": metrics["total_tokens"],
                        "response_time_seconds": metrics["duration_seconds"],
                    }
                )
                st.markdown("**First token logprobs**")
                st.write(metrics["first_token_logprobs"])

                st.markdown("**Response text**")
                st.markdown(metrics["text"])

    st.markdown("---")
    st.caption("The OpenAI API key stays in session memory only.")


if __name__ == "__main__":
    main()
