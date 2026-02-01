import yfinance as yf
import pandas as pd

tickers = {
    "ONGC": "ONGC.NS",
    "RELIANCE": "RELIANCE.NS",
    "IOC": "IOC.NS",
    "BPCL": "BPCL.NS",
    "GAIL": "GAIL.NS"
}

all_prices = []

for company, ticker in tickers.items():
    df = yf.download(ticker, start="2016-01-01", interval="3mo", auto_adjust=True, progress=False)
    df = df.reset_index()
    
    # Flatten columns if they are multi-level
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df["Company"] = company
    
    # Select only the columns we need
    df = df[["Company", "Date", "Close"]].copy()
    
    all_prices.append(df)

stocks = pd.concat(all_prices, ignore_index=True).sort_values(["Company", "Date"]).reset_index(drop=True)

# Calculate percentage return for each company
stocks['Return'] = None

for company in stocks['Company'].unique():
    mask = stocks['Company'] == company
    stocks.loc[mask, 'Return'] = stocks.loc[mask, 'Close'].pct_change() * 100

# Convert Return to numeric type
stocks['Return'] = pd.to_numeric(stocks['Return'])

stocks.to_csv("stock_prices.csv", index=False)

print(stocks.head(20))
print("\n")
print(stocks[stocks['Company'] == 'RELIANCE'].head(10))