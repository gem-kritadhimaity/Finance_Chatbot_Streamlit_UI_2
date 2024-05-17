import yfinance as yf
import pandas as pd

desired_date = '2023-09-30'

amzn = yf.Ticker("AMZN")
df1 = amzn.quarterly_income_stmt
df1.columns = pd.to_datetime(df1.columns, format='%Y-%m-%d')
desired_column1 = df1.loc[:, pd.to_datetime(desired_date, format='%Y-%m-%d')]

meta = yf.Ticker("META")
df2 = meta.quarterly_income_stmt
df2.columns = pd.to_datetime(df2.columns, format='%Y-%m-%d')
desired_column2 = df2.loc[:, pd.to_datetime(desired_date, format='%Y-%m-%d')]

aapl = yf.Ticker("AAPL")
df3 = aapl.quarterly_income_stmt
df3.columns = pd.to_datetime(df3.columns, format='%Y-%m-%d')
desired_column3 = df3.loc[:, pd.to_datetime(desired_date, format='%Y-%m-%d')]

goog = yf.Ticker("GOOG")
df4 = goog.quarterly_income_stmt
df4.columns = pd.to_datetime(df4.columns, format='%Y-%m-%d')
desired_column4 = df4.loc[:, pd.to_datetime(desired_date, format='%Y-%m-%d')]

combined_df = pd.concat([desired_column1, desired_column2, desired_column3, desired_column4], axis=1)
combined_df.columns = ["Amazon", "Meta", "Apple", "Alphabet"]

combined_df.to_csv("csvdata/combined_Q3_data.csv", index=True)

