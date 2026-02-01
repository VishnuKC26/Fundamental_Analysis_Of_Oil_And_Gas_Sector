import yfinance as yf
import pandas as pd

# Crude oil price (Brent)
oil = yf.download("BZ=F", start="2016-01-01", auto_adjust=True, progress=False)

oil_q = oil["Close"].resample("QE").last()

oil_change = oil_q.pct_change()

oil_df = oil_change.reset_index()
oil_df.columns = ["Date", "Oil_Change"]

oil_df.to_csv("brent_prices.csv", index=False)