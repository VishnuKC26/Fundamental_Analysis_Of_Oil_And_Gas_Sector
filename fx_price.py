import yfinance as yf
import pandas as pd

fx = yf.download("USDINR=X", start="2016-01-01", auto_adjust=True, progress=False)

fx_q = fx["Close"].resample("QE").last()

fx_change = fx_q.pct_change()

fx_df = fx_change.reset_index()
fx_df.columns = ["Date", "USDINR_Change"]

fx_df.to_csv("fx_prices.csv")
print(fx_df.head(10))

