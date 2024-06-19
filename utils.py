import os
from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
import os
from langchain_core.output_parsers import StrOutputParser

##
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq




# Initialize the llm variable globally
llm = None

def generate_sql_query(query,model):
    global llm
    if model == 'gemma-7b-it':
        llm = ChatGroq(temperature=0, model_name="gemma-7b-it")
    if model == 'mixtral-8x7b-32768':
        llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
    if model == 'llama3-70b-8192':
        llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    if model == 'llama3-8b-8192':
        llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
    # if model == 'gpt-3.5-turbo':
    #     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    nli_to_sql_prompt = ChatPromptTemplate.from_template(
    """
    You are a SQLite expert. 

    Given a table called data which contains following columns with their description:
    'Company Name', 'Tax Effect Of Unusual Items', 'Tax Rate For Calcs', 'Normalized EBITDA', 'Net Income From Continuing Operation Net Minority Interest', 'Reconciled Depreciation', 'Reconciled Cost Of Revenue', 'EBITDA', 'EBIT', 'Net Interest Income', 'Interest Expense', 'Interest Income', 'Normalized Income', 'Net Income From Continuing And Discontinued Operation', 'Total Expenses', 'Total Operating Income As Reported', 'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders', 'Net Income', 'Net Income Including Noncontrolling Interests', 'Net Income Continuous Operations', 'Tax Provision', 'Pretax Income', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net Non Operating Interest Income Expense', 'Interest Expense Non Operating', 'Interest Income Non Operating', 'Operating Income', 'Operating Expense', 'Research And Development', 'Selling General And Administration', 'Gross Profit', 'Cost Of Revenue', 'Total Revenue', 'Operating Revenue'

    Among the above colums most important columns are 'Company Name', 'Net Income', 'Total Expenses', 'Gross Profit', 'Total Revenue'

    Given an input question, create a correct SQL query to answer the question. 
    Never query for all columns from a table and only SELECT Company Name,Net Income, Total Expenses,Gross Profit,Total Revenue. Wrap each column name in double quotes (") to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the table's column description above. Be careful to not query for columns that do not exist.

    Key points to note:
    - if question says profit or net profit consider it as Gross Profit column in the table
    - consider company name as Amazon, Meta first letter should be uppercase
    - Auto-correct company name if necessary
    - always give revenue in the descending order of its value
    - when asked for top or bottom companies add LIMIT 10
    - when asked for the highest add LIMIT 1
    - when asked to compare among comanies, the sql query should search the table with the company mentioned to compare

    Input Question: {question}

    """
    )

    

    chain = nli_to_sql_prompt | llm | StrOutputParser()

    response = chain.invoke({'question': query})
    return response


def final_answer(question,sql_query,output):
    frame_answer_prompt = ChatPromptTemplate.from_template(
    """
    I'm asking a question regarding financial data of various companies. The Question gets converted into an sql query and I execute the query to get relevant results.
    Your task is to understand the question, sql query and its result and frame a suitable answer to the end user. Return the expected answer only and nothing else.

    Question: {question}
    SQL Query: {sql_query}
    Result from SQL Query: {output}

    Answer:
    """
    )
    chain_2 = frame_answer_prompt | llm | StrOutputParser()

    res = chain_2.invoke({
    'question': {question},
    'sql_query':{sql_query},
    'output':{output}
    })
    return res
