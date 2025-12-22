# Import the libraries
import os
import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv

# Read OpenAI Key from the .ENV file
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API")

# Streamlit UI
st.title("Celebrity Searching Application")
input_text = st.text_input("Celebrity Name", placeholder="e.g., Elon Musk")

# ------- LANGCHAIN SETUP -------
# Initialise the Brain
llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0.8,
    max_completion_tokens=1000,
    timeout=300
)

# Define Output Parser - to cleanup messy JSON/HTML output to simple text
output_parser = StrOutputParser()

# STEP-1: Giving the about of the Celebrity
prompt_about = ChatPromptTemplate.from_template(
    "Write a 3-line engaging short and concise summary about the celebrity {name}"
)
chain_about = prompt_about | llm | output_parser

# STEP-2: Giving the Birth Year
prompt_dob = ChatPromptTemplate.from_template(
    "Based on the given discription, give me the birth year of the following celebrity {name}"
)
chain_dob = prompt_dob | llm | output_parser

# STEP-3: Historical Events on that birth year
prompt_history = ChatPromptTemplate.from_template(
    "From the above birth year {birth_year}, give me 5 important historical facts which happened all across the world"
)
chain_history = prompt_history | llm | output_parser

# ------- EXECUTION FLOW -------
if input_text:
    with st.spinner(f"Searching for {input_text}", show_time=True):
        time.sleep(2)
        about_result = chain_about.invoke({'name':input_text})
        with st.expander(f"{input_text} biography"):
            st.info(about_result)
        
        dob_result = chain_dob.invoke({'name':input_text})
        with st.expander(f"{input_text}'s Birth Year"):
            st.info(dob_result)
        
        history_result = chain_history.invoke({'birth_year':dob_result})
        with st.expander(f"5 Important Historical Facts on {dob_result}"):
            st.info(history_result)