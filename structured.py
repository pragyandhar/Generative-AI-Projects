# IMPORT
from pydantic import BaseModel
from typing import List

# SCHEMA DEFINITION
class Lesson(BaseModel):
    topic: str
    steps: List[str]
    examples: List[str]
    quiz: List[str]

# BINDING THE SCHEMA TO THE MODEL
from langchain_openai import ChatOpenAI

api = ""

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    api_key = api,
    temperature = 0.5,
    max_completion_tokens = 2000
)

structured_output = llm.with_structured_output(Lesson)

# INVOKING AND GETTING THE STRUCTURED OUTPUT
from langchain_core.messages import HumanMessage

def get_lesson(topic: str):
    """
    This generates the lesson around the given topic in a structured format
    """
    prompt = f"Get lessons on this topic: {topic}"
    result = structured_output.invoke([HumanMessage(content=prompt)])
    return {
        "topic": result.topic,
        "steps": result.steps,
        "examples": result.examples,
        "quiz": result.quiz
    }