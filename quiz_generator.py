'''quiz_generator.py'''
# IMPORT
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# TOOL MAKING
@tool
def quiz_generator(topic: str):
    '''
    This tool generates quiz of 5 questions regarding the topic. The questions are in increasing order of difficulty.

    Args: 
        Topic: Enter the topic around which you want to generate quiz
    '''
    api = ""

    tool_model = ChatOpenAI(
        model = "gpt-4o-mini",
        api_key = api,
        temperature = 0.5,
        max_completion_tokens = 2000
    )

    prompt = f"""
    Create 5 quiz questions about this topic: {topic}
    - Questions should range from easy to hard
    - Number them 1 to 5
    """

    response = tool_model.invoke([HumanMessage(content=prompt)])
    return response.content