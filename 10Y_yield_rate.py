import pandas as pd

rates = pd.read_csv("10yr_Bond.csv")

# Parse date (day-first format)
rates["Date"] = pd.to_datetime(rates["Date"], dayfirst=True)

# Convert Price to numeric
rates["Price"] = rates["Price"].astype(str).str.replace(",", "").astype(float)

# Set Date as index
rates = rates.set_index("Date").sort_index()

rate_q = rates["Price"].resample("Q").last()

rate_change = rate_q.diff()

rate_df = rate_change.reset_index()
rate_df.columns = ["Date", "Rate_Change"]

rate_df.to_csv("10Y_yield_rate.csv")
print(rate_df.head(10))