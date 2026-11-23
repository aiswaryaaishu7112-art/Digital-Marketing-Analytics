
import pandas as pd
import numpy as np
import os

# Project paths
base_folder = r"C:\Digital_Marketing_Analytics"

input_file = os.path.join(
    base_folder, "dataset", "cleaned_marketing_data.csv"
)

output_folder = os.path.join(
    base_folder, "visualizations"
)

os.makedirs(output_folder, exist_ok=True)

# Load cleaned dataset
if not os.path.exists(input_file):
    raise FileNotFoundError(
        "Cleaned dataset not found. Run data_cleaning.py first."
    )

df = pd.read_csv(input_file)

print("Dataset loaded successfully!")
print("Total records:", len(df))

if df.empty:
    raise ValueError("The cleaned dataset is empty.")

# Safe division function
def safe_divide(numerator, denominator):
    return np.where(
        denominator > 0,
        numerator / np.where(denominator > 0, denominator, 1),
        0
    )

# Calculate row-level performance metrics
df["CTR"] = safe_divide(
    df["clicks"], df["impressions"]
) * 100

df["CPC"] = safe_divide(
    df["spend"], df["clicks"]
)

df["Conversion_Rate"] = safe_divide(
    df["conversions"], df["clicks"]
) * 100

df["CPA"] = safe_divide(
    df["spend"], df["conversions"]
)

df["ROAS"] = safe_divide(
    df["revenue"], df["spend"]
)

# Overall performance
total_impressions = df["impressions"].sum()
total_clicks = df["clicks"].sum()
total_spend = df["spend"].sum()
total_conversions = df["conversions"].sum()
total_revenue = df["revenue"].sum()

overall_ctr = safe_divide(
    total_clicks, total_impressions
).item() * 100

overall_cpc = safe_divide(
    total_spend, total_clicks
).item()

overall_conversion_rate = safe_divide(
    total_conversions, total_clicks
).item() * 100

overall_cpa = safe_divide(
    total_spend, total_conversions
).item()

overall_roas = safe_divide(
    total_revenue, total_spend
).item()

print("\n========== OVERALL MARKETING PERFORMANCE ==========")

print("Total Impressions:", total_impressions)
print("Total Clicks:", total_clicks)
print("Total Spend:", round(total_spend, 2))
print("Total Conversions:", total_conversions)
print("Total Revenue:", round(total_revenue, 2))
print("Overall CTR:", round(overall_ctr, 2), "%")
print("Overall CPC:", round(overall_cpc, 2))
print("Overall Conversion Rate:", round(overall_conversion_rate, 2), "%")
print("Overall CPA:", round(overall_cpa, 2))
print("Overall ROAS:", round(overall_roas, 2))

# Channel-wise performance
channel_performance = df.groupby("channel").agg({
    "impressions": "sum",
    "clicks": "sum",
    "spend": "sum",
    "conversions": "sum",
    "revenue": "sum"
}).reset_index()

channel_performance["CTR"] = safe_divide(
    channel_performance["clicks"],
    channel_performance["impressions"]
) * 100

channel_performance["CPC"] = safe_divide(
    channel_performance["spend"],
    channel_performance["clicks"]
)

channel_performance["Conversion_Rate"] = safe_divide(
    channel_performance["conversions"],
    channel_performance["clicks"]
) * 100

channel_performance["CPA"] = safe_divide(
    channel_performance["spend"],
    channel_performance["conversions"]
)

channel_performance["ROAS"] = safe_divide(
    channel_performance["revenue"],
    channel_performance["spend"]
)

print("\n========== CHANNEL-WISE PERFORMANCE ==========")
print(channel_performance.round(2).to_string(index=False))

# Campaign-wise performance
# Grouping by channel as well ensures dashboard filters work correctly.
campaign_performance = df.groupby(
    ["campaign", "channel"]
).agg({
    "impressions": "sum",
    "clicks": "sum",
    "spend": "sum",
    "conversions": "sum",
    "revenue": "sum"
}).reset_index()

campaign_performance["CTR"] = safe_divide(
    campaign_performance["clicks"],
    campaign_performance["impressions"]
) * 100

campaign_performance["CPC"] = safe_divide(
    campaign_performance["spend"],
    campaign_performance["clicks"]
)

campaign_performance["Conversion_Rate"] = safe_divide(
    campaign_performance["conversions"],
    campaign_performance["clicks"]
) * 100

campaign_performance["CPA"] = safe_divide(
    campaign_performance["spend"],
    campaign_performance["conversions"]
)

campaign_performance["ROAS"] = safe_divide(
    campaign_performance["revenue"],
    campaign_performance["spend"]
)

print("\n========== CAMPAIGN-WISE PERFORMANCE ==========")
print(campaign_performance.round(2).to_string(index=False))

# Best performing channel
best_channel = channel_performance.loc[
    channel_performance["ROAS"].idxmax()
]

print("\n========== BEST PERFORMING CHANNEL ==========")
print("Channel:", best_channel["channel"])
print("ROAS:", round(best_channel["ROAS"], 2))

# Best performing campaign
campaign_summary = df.groupby("campaign").agg({
    "spend": "sum",
    "revenue": "sum",
    "conversions": "sum"
}).reset_index()

campaign_summary["ROAS"] = safe_divide(
    campaign_summary["revenue"],
    campaign_summary["spend"]
)

best_campaign = campaign_summary.loc[
    campaign_summary["ROAS"].idxmax()
]

print("\n========== BEST PERFORMING CAMPAIGN ==========")
print("Campaign:", best_campaign["campaign"])
print("ROAS:", round(best_campaign["ROAS"], 2))

# Save all three CSV files
df.to_csv(
    os.path.join(output_folder, "marketing_metrics.csv"),
    index=False
)

channel_performance.to_csv(
    os.path.join(output_folder, "channel_performance.csv"),
    index=False
)

campaign_performance.to_csv(
    os.path.join(output_folder, "campaign_performance.csv"),
    index=False
)

print("\n==========================================")
print("MARKETING ANALYSIS COMPLETED SUCCESSFULLY!")
print("==========================================")

print("Saved files:")
print("1. marketing_metrics.csv")
print("2. channel_performance.csv")
print("3. campaign_performance.csv")
print("Output folder:", output_folder)
