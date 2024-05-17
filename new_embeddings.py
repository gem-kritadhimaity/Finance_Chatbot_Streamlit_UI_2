from langchain_community.embeddings import SentenceTransformerEmbeddings
from huggingface_hub import InferenceClient 
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import CSVLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import pandas as pd
 
embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
persist_directory = 'csv_text_db'
# csv_texts = "csvdata/combined_Q3_data.csv"
# Create Chroma database


csv_loader = CSVLoader("csvdata/combined_Q3_data.csv", encoding="windows-1252")
csv_documents  = csv_loader.load()

text_loader_kwargs={'autodetect_encoding': True}
directory_loader = DirectoryLoader('./texts/', glob="./*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
text_documents = directory_loader.load()

# Split text documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
text_chunks = text_splitter.split_documents(text_documents)

combined_documents = csv_documents + text_chunks

# Create Chroma database from documents
chroma_db = Chroma.from_documents(embedding=embeddings, documents=combined_documents, persist_directory=persist_directory)


