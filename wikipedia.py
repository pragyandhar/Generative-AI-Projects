'''wikipedia.py'''
# IMPORTS
import wikipedia

from langchain.tools import tool

# TOOLS MAKING
@tool
def wikipedia_lookup(query: str):
    """
    Give a short summary around the query
    """
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return "No result found"