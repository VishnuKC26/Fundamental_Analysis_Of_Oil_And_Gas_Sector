import pandas as pd

# -----------------------------
# 1. Load MOSPI CSV
# -----------------------------

df = pd.read_csv("IIP_growth_rates.csv")

print("Shape:", df.shape)
print(df.head())

# -----------------------------
# 2. Extract GENERAL IIP row
# -----------------------------

general = df[df["Activities"].str.strip() == "General"]

if general.empty:
    raise ValueError("General row not found")

# -----------------------------
# 3. Drop non-month columns
# -----------------------------

month_cols = df.columns[3:]   # everything after Weights

growth_row = general[month_cols].iloc[0]

# -----------------------------
# 4. Convert to long time series
# -----------------------------

iip_monthly = growth_row.reset_index()
iip_monthly.columns = ["Month", "IIP_Growth"]

# Convert Month like "Apr-12" to datetime
iip_monthly["Date"] = pd.to_datetime(
    iip_monthly["Month"],
    format="%b-%y"
)

iip_monthly["IIP_Growth"] = pd.to_numeric(iip_monthly["IIP_Growth"], errors="coerce")

iip_monthly = iip_monthly[["Date", "IIP_Growth"]].sort_values("Date")

print("\nMonthly IIP growth:")
print(iip_monthly.head())

# -----------------------------
# 5. Convert monthly → quarterly demand shock
# -----------------------------

iip_monthly = iip_monthly.set_index("Date")

# Average growth in each quarter (standard macro method)
iip_quarterly = iip_monthly["IIP_Growth"].resample("QE").mean()

iip_df = iip_quarterly.reset_index()
iip_df.columns = ["Date", "IIP_Growth"]

print("\nQuarterly IIP growth:")
print(iip_df.head(10))

# -----------------------------
# 6. Save clean output
# -----------------------------

iip_df.to_csv("iip_quarterly.csv", index=False)

print("\nSaved as iip_quarterly.csv")
