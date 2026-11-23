
import pandas as pd
import os

# Dataset path
file_path = r"C:\Digital_Marketing_Analytics\dataset\sample-marketing.csv"

# Check dataset
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Dataset not found: {file_path}")

print("Loading dataset:", os.path.basename(file_path))

df = pd.read_csv(file_path)

# First 10 records
print("\n========== FIRST 10 RECORDS ==========")
print(df.head(10).to_string())

# Dataset dimensions
print("\n========== DATASET SIZE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# Data types
print("\n========== DATA TYPES ==========")
print(df.dtypes)

# Missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# Duplicate records
print("\n========== DUPLICATE RECORDS ==========")
print("Duplicates:", df.duplicated().sum())

# Statistical summary
print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all").to_string())

print("\nDATA EXPLORATION COMPLETED SUCCESSFULLY!")
