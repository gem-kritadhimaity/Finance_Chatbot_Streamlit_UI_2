# from langchain_experimental.agents import create_csv_agent
# # from langchain.llms import OpenAI
# from langchain_community.embeddings import SentenceTransformerEmbeddings
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
import re
from utils import generate_sql_query,final_answer
import streamlit as st
 

def connect_to_database(db_name='final_data.db', table_name='data'):
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
@st.cache_data
def query(query,model):
    query = query.replace("net", "").replace("Net", "")
    sql_query = parse_sql_query(generate_sql_query(query,model))
    print(sql_query)
    results = run_query(sql_query)
    answer = final_answer(query,sql_query,output=results)
    print(answer)
    return answer


