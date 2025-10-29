import pandas as pd

# Load CSV
file_path = "all_apps_data.csv"
df = pd.read_csv(file_path)

# Drop first two rows ("Daily Data" and duplicate header)
df = df.iloc[2:].reset_index(drop=True)

# Drop completely empty columns (like Unnamed: 0)
df = df.dropna(axis=1, how='all')

# 🔍 Check how many columns remain
print("Columns detected:", len(df.columns))
print("Column names:", df.columns.tolist())

# Now safely rename (only if 11 columns)
df.columns = [
    "Date", "unique_idfas", "unique_ips", "unique_uas", "total_requests",
    "requests_per_idfa", "impressions", "impressions_per_idfa",
    "idfa_ip_ratio", "idfa_ua_ratio", "IVT"
]

# Convert numeric columns
numeric_cols = [
    "unique_idfas", "unique_ips", "unique_uas", "total_requests",
    "requests_per_idfa", "impressions", "impressions_per_idfa",
    "idfa_ip_ratio", "idfa_ua_ratio", "IVT"
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop blank rows
df = df.dropna(subset=["Date"]).reset_index(drop=True)

# ✅ Final check
print(df.head())
print(df.info())


# -------------------------------------------Basic Statistical Summary--------------------------------------

print("\n=== Summary Statistics ===")
print(df.describe())

# Correlation matrix (helps spot relationships between metrics)
print("\n=== Correlation Matrix ===")
print(df.corr())




# ----------------------------------------------Visualize Key Patterns--------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create folder for graphs if it doesn't exist
os.makedirs("graphs", exist_ok=True)

# Plot 1: IVT over time
plt.figure(figsize=(10, 6))
sns.lineplot(x="Date", y="IVT", data=df, marker="o")
plt.title("IVT Trend Over Time")
plt.xlabel("Date")
plt.ylabel("IVT (Invalid Traffic Ratio)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/ivt_trend.png")
plt.close()

# Plot 2: IDFA-UA Ratio vs IVT
plt.figure(figsize=(8, 6))
sns.scatterplot(x="idfa_ua_ratio", y="IVT", data=df)
plt.title("Relationship between IDFA-UA Ratio and IVT")
plt.xlabel("IDFA-UA Ratio")
plt.ylabel("IVT")
plt.tight_layout()
plt.savefig("graphs/idfa_ua_vs_ivt.png")
plt.close()

# Plot 3: Requests per IDFA vs IVT
plt.figure(figsize=(8, 6))
sns.scatterplot(x="requests_per_idfa", y="IVT", data=df)
plt.title("Requests per IDFA vs IVT")
plt.xlabel("Requests per IDFA")
plt.ylabel("IVT")
plt.tight_layout()
plt.savefig("graphs/requests_per_idfa_vs_ivt.png")
plt.close()

print("✅ Graphs saved in the 'graphs' folder.")



# -------Interpret the Results-------Look for:High IVT values,idfa_ua_ratio spikes,requests_per_idfa-------


ivt_high = df[df["IVT"] > 0.8]
print("\n=== Days with High IVT ===")
print(ivt_high[["Date", "idfa_ua_ratio", "idfa_ip_ratio", "requests_per_idfa", "IVT"]])




# -------------------Highlight Anomalies--------------------------------------------------


# Identify anomalies (very high idfa_ua_ratio or idfa_ip_ratio)
anomalies = df[
    (df["idfa_ua_ratio"] > df["idfa_ua_ratio"].mean() + 2 * df["idfa_ua_ratio"].std()) |
    (df["idfa_ip_ratio"] > df["idfa_ip_ratio"].mean() + 2 * df["idfa_ip_ratio"].std())
]
print("\n=== Potential Anomaly Days ===")
print(anomalies[["Date", "idfa_ua_ratio", "idfa_ip_ratio", "IVT"]])
