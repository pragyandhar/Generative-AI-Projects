import os
import requests
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool

WEATHER_KEY = os.getenv("WEATHER_API_KEY")

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    if not WEATHER_KEY:
        return f"{location}: Weather API key not configured"
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key={WEATHER_KEY}&contentType=json"
    try:
        r = requests.get(url).json()
        temp = r['currentConditions']['temp']
        conditions = r['currentConditions']['conditions']
        return f"{location}: {temp}°C, {conditions}"
    except Exception as e:
        return f"{location}: Unable to fetch weather data - {str(e)}"

def weather_agent(query: str):
    base_model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    # Bind Tools
    agent_model = base_model.bind_tools([get_weather])
    messages = [HumanMessage(content=query)]

    # Model generates tool call
    ai_message = agent_model.invoke(messages)
    messages.append(ai_message)

    # get the tool call result
    for call in ai_message.tool_calls:
        tool_result = get_weather.invoke(call)
        messages.append(tool_result)

    # final model response
    final = agent_model.invoke(messages)
    return {"response": final.text}