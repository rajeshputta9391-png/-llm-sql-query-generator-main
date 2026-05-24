import streamlit as st
import sqlite3
import openai
import os
from dotenv import load_dotenv
from query_generator import generate_sql, load_db_schema
from sql_validator import validate_sql, execute_test_query

st.title("LLM-Based SQL Query Generator")

st.sidebar.header("Project Settings")

# Load API key from .env
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

api_key = st.sidebar.text_input("OpenAI API Key",value=OPENAI_API_KEY,type = "password")

if api_key:
    openai.api_key = api_key
    st.sidebar.success("Api Key Set!")
else:
    st.sidebar.warning("Please enter you OpenAI API Key to proceed.")

db_path = st.sidebar.text_input("Database Path","data/spider_data/database/coffee_shop/coffee_shop.sqlite")

natural_language_query = st.text_area("Enter your natural language query: ", "")


# Initialize session state for sql_query if not set
if "sql_query" not in st.session_state:
    st.session_state["sql_query"] = ""

if st.button("Generate SQL"):
    if natural_language_query.strip():
        st.session_state["sql_query"] = generate_sql(load_db_schema(db_path),natural_language_query)
    else:
        st.session_state["sql_query"] = ""
        st.warning("Please enter a query.")
        

st.subheader("Generated SQL Query")
# Always display the stored SQL query
if st.session_state["sql_query"]:
    st.code(st.session_state["sql_query"], language="sql")


if st.button("Validate & Execute"):
    if  st.session_state["sql_query"]:
        is_valid, validation_msg = validate_sql(st.session_state["sql_query"])
        if is_valid:
            st.success("✅ SQL is valid!")
            success, result = execute_test_query(st.session_state["sql_query"],db_path)
            if success:
                st.dataframe(result)
            else:
                st.error(f"Execution Error: {result}")
        else:
            st.error(f"Invalid SQL: {validation_msg}")
    else:
        st.warning("Generate a query first!")