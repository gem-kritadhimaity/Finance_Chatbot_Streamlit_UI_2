import csv
import os
from langchain.docstore.document import Document 
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


#os open ai api key line 

columns_to_embed = ["Company Name","Gross Profit", "Total Revenue","EBITDA","Total Expenses" ]
columns_to_metadata = ["Company Name",	"Tax Effect Of Unusual Items"	,"Tax Rate For Calcs"	, 'Normalized EBITDA',	'Total Unusual Items'	,'Total Unusual Items Excluding Goodwill',	'Net Income From Continuing Operation', 'Net Minority Interest',	'Reconciled Depreciation'	,'Reconciled' ,"Cost Of Revenue",	"EBITDA"	,"EBIT",	"Net Interest Income"	,"Interest Expense",	"Interest Income",	"Normalized Income","Net Income From Continuing And Discontinued Operation",	"Total Expenses"	,"Total Operating Income As Reported"	,"Diluted Average Shares"	,"Basic Average Shares",	"Diluted EPS"	,"Basic EPS"	,"Diluted NI Availto Com Stockholders"	,"Net Income Common Stockholders"	,"Net Income"	,"Net Income Including Noncontrolling Interests",	"Net Income Continuous Operations"	,"Earnings From Equity Interest Net Of Tax"	,"Tax Provision",	"Pretax Income""Other Income Expense"	,"Other Non Operating Income Expenses",	"Gain On Sale Of Security",	'Net Non Operating Interest Income Expense'	,"Interest Expense Non Operating"	,"Interest Income Non Operating",	"Operating Income",	"Operating Expense",	"Other Operating Expenses"	,'Selling General And Administration'	,"Selling And Marketing Expense",	"General And Administrative Expense	Other Gand A"	,"Gross Profit"	,"Cost Of Revenue"	,"Total Revenue"	,"Operating Revenue",	"Average Dilution Earnings"	,"Total Other Finance Cost"	,"Research And Development"	,"Earnings From Equity Interest"]

docs = []
with open("csvdata/70_combined_Q3_data.csv", newline="", encoding='utf-8-sig') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for i, row in enumerate(csv_reader):
        to_metadata = {col: row[col] for col in columns_to_metadata if col in row}
        values_to_embed = {k: row[k] for k in columns_to_embed if k in row}
        to_embed = "\n".join(f"{k.strip()}: {v.strip()}" for k, v in values_to_embed.items())
        # newDoc = Document(page_content=to_embed, metadata=to_metadata)
        docs.append(to_embed)

total_string = "\n".join(docs)
print(total_string)
splitter = RecursiveCharacterTextSplitter(
                                # separator = "\n",
                                chunk_size=2000, 
                                chunk_overlap=10,
                                # length_function=len
                                )
documents = splitter.split_text(total_string)

# print(type(documents))

embeddings_model = OpenAIEmbeddings()
db = Chroma.from_texts(documents, OpenAIEmbeddings(), persist_directory="csv1_data_vectordb")

print(len(documents))
print("Done")
