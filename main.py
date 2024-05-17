import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
import re
from utils import generate_sql_query,final_answer


# Function to create SQLDatabase instance from existing SQLite database
def connect_to_database(db_name='1_data.db', table_name='data'):
    # Create SQLite engine
    engine = create_engine(f"sqlite:///{db_name}")

    # Create SQLDatabase instance
    db = SQLDatabase(engine=engine)

    return db

def parse_sql_query(query):
    # Check if query is inside sql  tags
    if "```sql" in query and "```" in query:
        # Extract the SQL query using regex
        sql_query = re.search(r'```sql\s*(.*?)\s*```', query, re.DOTALL)
        if sql_query:
            return sql_query.group(1).strip()
    # If not inside sql  tags, return the query as it is
    return query.strip()

def run_query(query):
    try:
        results_df = db.run(query)
        return results_df
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Connect to existing database and create SQLDatabase instance
db = connect_to_database()

# Streamlit app
st.title("SQLite Database Query App")

# Input for SQL query
query = st.text_input("Enter Query:")

query = query.replace("net", "").replace("Net", "")

# query = "Give me the names of top rom com movies for last 4 year"
sql_query = parse_sql_query(generate_sql_query(query))
print(sql_query)

# Button to execute query
if st.button("Run Query"):
    if sql_query:
        results = run_query(sql_query)
        # st.write(results)
        ans=final_answer(query,sql_query,output=results)
        # # selected_list = ast.literal_eval(results)
        # # df_results = pd.DataFrame(selected_list) # This will print the JSON object
        st.write(ans)
    else:
        st.warning("Please enter an SQL query.")