from openai import OpenAI
import os
from dotenv import load_dotenv
import sqlparse
import sqlite3

# Load API key from .env
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # make sure to have your OPENAI API key saved in the .env file

OPENAI_model = "gpt-4"
openai = OpenAI()   



# Creating messages list to feed to API
def prompt_for(db_schema,nlp_query):
    system_prompt = f"""
    You are an assistant which takes an input a query written in natural language
    and converts this into a well structured SQL query.
    The schema of the database is: {db_schema}
    Do not provide or explaination of the query, just the query.
    """
    user_prompt = f"Convert the following request into an SQL query: {nlp_query}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return messages

# Generates an SQL query from natural language input using above defined model
def generate_sql(db_schema,nlp_query):
    messages = prompt_for(db_schema,nlp_query)

    # Call OpenAI
    response = openai.chat.completions.create(
        model=OPENAI_model, messages=messages, temperature=0.1
    )

    return response.choices[0].message.content

def validate_sql(query):
    try:
        parsed = sqlparse.parse(query)
        if not parsed:
            return False, "Invalid SQL syntax."
        return True, "SQL is valid"
    except Exception as e:
        return False, str(e)
    
def execute_test_query(query, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True, "SQL executed successfully"
    except Exception as e:
        return False, str(e)
    
def load_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    schema = "\n".join(row[0] for row in cursor.fetchall() if row[0])
    
    conn.close()
    return schema

if __name__ == "__main__":
    user_query = "Select all directors born before 1980."
    db_path = "data/spider_data/database/imdb/imdb.sqlite"
    sql_query = generate_sql(load_db_schema(db_path),user_query)
    print(sql_query)

    valid, msg = validate_sql(sql_query)
    print("\nValidation Result:\n", msg)

    if valid:
        executed, exec_msg = execute_test_query(sql_query,db_path)
        print("\nExecution Test:\n", exec_msg)