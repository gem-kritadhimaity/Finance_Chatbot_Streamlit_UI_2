import yfinance as yf
import pandas as pd

# Define the desired date
desired_date = '2023-09-30'

# Define a list of top 100 US tech companies (example list)
top_100_tech_companies = ["AAPL", "MSFT", "GOOG", "GOOGL", "FB", "TSLA", "NVDA", "ADBE", "INTC", "CSCO", 
                          "ASML", "PYPL", "CMCSA", "NFLX", "SAP", "ABNB", "BABA", "AMZN", "TSM", "TMUS",
                          "ORCL", "AVGO", "CRM", "QCOM", "UBER", "TXN", "SHOP", "IBM", "SQ", "AMD",
                          "BIDU", "LRCX", "NET", "ZM", "SNOW", "U", "LMT", "JD", "CRWD", "TWLO",
                          "NOW", "TEAM", "DOCU", "ZTS", "PDD", "SE", "SNE", "NTDOY", "NET", "U",
                          "INTU", "AMAT", "MRNA", "ROKU", "CHTR", "ADI", "DELL", "FISV", "DDOG",
                          "MDB", "KLAC", "NIO", "PTON", "OKTA", "SPLK", "VRSN", "NTES", "SNAP",
                          "DDOG", "NVCR", "FSLY", "TWTR", "MELI", "CRSP", "ALGN", "CRSR", "AYX",
                          "PINS", "ZG", "WDC", "MPWR", "Z", "PLTR", "ECL", "VRTX", "EBAY", "SWKS",
                          "COST", "RNG", "DXCM", "CDNS", "WIX", "FTNT", "PANW", "SWI", "LULU"]

# Initialize an empty DataFrame to store combined data
combined_df = pd.DataFrame()

# Loop through each company
for company_symbol in top_100_tech_companies:
    # Fetch quarterly income statement data for the company
    company = yf.Ticker(company_symbol)
    df = company.quarterly_income_stmt
    df.columns = pd.to_datetime(df.columns, format='%Y-%m-%d')
    
    # Extract the desired column for the desired date
    desired_column = df.loc[:, pd.to_datetime(desired_date, format='%Y-%m-%d')]
    
    # Append the data to the combined DataFrame
    combined_df[company_symbol] = desired_column

# Rename columns with company symbols
combined_df.columns = top_100_tech_companies

# Export the combined DataFrame to an Excel file
combined_df.to_csv("csvdata\combined_Q3_data.csv", index=True)