from openai import OpenAI
import os
from dotenv import load_dotenv
import sqlite3

# Load API key from .env
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Use a model accessible to all API keys
OPENAI_MODEL = "gpt-4o-mini"

# ----- Prompt Builder -----
def prompt_for(db_schema, nlp_query):
    system_prompt = f"""
    You are an expert SQL query generator.
    Convert natural language queries into valid SQLite SQL queries.
    Database Schema:
    {db_schema}
    Do not provide explanation. Return only SQL query.
    """

    user_prompt = f"Convert this request into SQL: {nlp_query}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return messages


# ----- Generate SQL from Natural Language -----
def generate_sql(db_schema, nlp_query):
    messages = prompt_for(db_schema, nlp_query)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.1
    )

    return response.choices[0].message.content.strip()


# ----- Load Database Schema -----
def load_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schema = "\n".join(row[0] for row in cursor.fetchall() if row[0])

    conn.close()
    return schema


# ----- Test Block -----
if __name__ == "__main__":
    user_query = "Show all employees"
    db_path = "database.db"   # your sample database
    sql_query = generate_sql(load_db_schema(db_path), user_query)
    print(sql_query)
