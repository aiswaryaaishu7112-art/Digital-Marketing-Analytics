
import pandas as pd
import os

# Project paths
base_folder = r"C:\Digital_Marketing_Analytics"
input_file = os.path.join(
    base_folder, "dataset", "sample-marketing.csv"
)
output_file = os.path.join(
    base_folder, "dataset", "cleaned_marketing_data.csv"
)

# Check dataset
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Dataset not found: {input_file}")

# Load original dataset
df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)

# Required columns
required_columns = [
    "date",
    "channel",
    "campaign",
    "impressions",
    "clicks",
    "spend",
    "conversions",
    "revenue"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# 1. Remove duplicate records
df = df.drop_duplicates()

# 2. Convert date column
df["date"] = pd.to_datetime(
    df["date"], errors="coerce"
)

# 3. Clean text columns
df["channel"] = df["channel"].astype("string").str.strip()
df["campaign"] = df["campaign"].astype("string").str.strip()

# 4. Convert numerical columns
numeric_columns = [
    "impressions",
    "clicks",
    "spend",
    "conversions",
    "revenue"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# 5. Check missing values
print("\nMissing values before removal:")
print(df[required_columns].isnull().sum())

# 6. Remove invalid or missing required values
df = df.dropna(subset=required_columns)

# 7. Remove empty channel and campaign names
df = df[
    (df["channel"] != "") &
    (df["campaign"] != "")
]

# 8. Validate numerical data
df = df[
    (df["impressions"] >= 0) &
    (df["clicks"] >= 0) &
    (df["spend"] >= 0) &
    (df["conversions"] >= 0) &
    (df["revenue"] >= 0)
]

# 9. Check cleaned dataset
print("\nCleaned dataset shape:", df.shape)

print("\nMissing values after cleaning:")
print(df[required_columns].isnull().sum())

# 10. Save cleaned dataset
os.makedirs(os.path.dirname(output_file), exist_ok=True)

df.to_csv(output_file, index=False)

print("\nDATA CLEANING COMPLETED SUCCESSFULLY!")
print("Cleaned dataset saved at:", output_file)

print("\nFinal dataset preview:")
print(df.head(10).to_string())
