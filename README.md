LLM-Based SQL Query Generator
Project Overview

This project is an AI-powered SQL Query Generator that translates natural language queries into SQL statements using GPT-4. It helps users generate, validate, and execute SQL queries against a specified database schema.

Developed by PUTTA RAJESHKUMAR
GitHub[:https://github.com/rajeshputta9391]

User Interface

Features

Natural Language to SQL: Uses OpenAI's GPT-4 to generate SQL queries.

Query Validation: Ensures generated queries are syntactically correct.

Database Execution: Runs SQL queries against an SQLite database.

Custom Schema Support: GPT generates SQL based on your database schema.

User-Friendly UI: Built with Streamlit for ease of use.

Secure API Key Management: Users can input their OpenAI API Key manually or load it from a .env file.

Tech Stack

Backend: Python, OpenAI API, SQLite

Frontend: Streamlit

Libraries: SQL Parsing, python-dotenv

🚀 Installation & Setup
1️. Clone the Repository
https://github.com/rajeshputta9391-png/-llm-sql-query-generator-main.git
cd llm-sql-query-generator
2. Install Dependencies
pip install -r requirements.txt
3. Set Up the .env File

Create a .env file in the root directory and add your OpenAI API Key:

OPENAI_API_KEY=your_openai_api_key_here
4. Run the Streamlit App
streamlit run src/app.py
Usage

Enter your OpenAI API Key in the Project Settings section or let it load from .env.

Provide the database path to your SQLite file.

Enter a natural language query (e.g., "Show all employees who joined after 2020").

Click Generate SQL to get the SQL query.

Validate & Execute the query to see the results.

Contributing

Pull requests are welcome! If you’d like to contribute, please open an issue first to discuss your changes.
