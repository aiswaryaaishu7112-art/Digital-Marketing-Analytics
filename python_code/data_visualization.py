
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Project paths
base_folder = r"C:\Digital_Marketing_Analytics"
input_folder = os.path.join(base_folder, "visualizations")
graph_folder = os.path.join(input_folder, "graphs")

os.makedirs(graph_folder, exist_ok=True)

# Load analysis results
channel_file = os.path.join(
    input_folder, "channel_performance.csv"
)
campaign_file = os.path.join(
    input_folder, "campaign_performance.csv"
)
metrics_file = os.path.join(
    input_folder, "marketing_metrics.csv"
)

for file in [channel_file, campaign_file, metrics_file]:
    if not os.path.exists(file):
        raise FileNotFoundError(
            f"{file} not found. Run marketing_analysis.py first."
        )

channel_df = pd.read_csv(channel_file)
campaign_df = pd.read_csv(campaign_file)
metrics_df = pd.read_csv(metrics_file)

print("Datasets loaded successfully!")

sns.set_theme(style="whitegrid")

# 1. Channel-wise Revenue
plt.figure(figsize=(10, 6))

sns.barplot(
    data=channel_df,
    x="channel",
    y="revenue"
)

plt.title("Channel-wise Revenue Comparison")
plt.xlabel("Marketing Channel")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(graph_folder, "channel_revenue.png"),
    dpi=300
)
plt.close()

# 2. Channel-wise ROAS
plt.figure(figsize=(10, 6))

sns.barplot(
    data=channel_df,
    x="channel",
    y="ROAS"
)

plt.title("Channel-wise Return on Ad Spend (ROAS)")
plt.xlabel("Marketing Channel")
plt.ylabel("ROAS")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(graph_folder, "channel_roas.png"),
    dpi=300
)
plt.close()

# 3. Campaign-wise Revenue
campaign_revenue = campaign_df.groupby(
    "campaign", as_index=False
)["revenue"].sum()

plt.figure(figsize=(12, 6))

sns.barplot(
    data=campaign_revenue,
    x="campaign",
    y="revenue"
)

plt.title("Campaign-wise Revenue Comparison")
plt.xlabel("Campaign")
plt.ylabel("Revenue")
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig(
    os.path.join(graph_folder, "campaign_revenue.png"),
    dpi=300
)
plt.close()

# 4. Campaign-wise Conversions
campaign_conversions = campaign_df.groupby(
    "campaign", as_index=False
)["conversions"].sum()

plt.figure(figsize=(12, 6))

sns.barplot(
    data=campaign_conversions,
    x="campaign",
    y="conversions"
)

plt.title("Campaign-wise Conversion Comparison")
plt.xlabel("Campaign")
plt.ylabel("Conversions")
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig(
    os.path.join(graph_folder, "campaign_conversions.png"),
    dpi=300
)
plt.close()

# 5. Marketing Spend vs Revenue
plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=metrics_df,
    x="spend",
    y="revenue",
    hue="channel",
    s=80
)

plt.title("Marketing Spend vs Revenue")
plt.xlabel("Marketing Spend")
plt.ylabel("Revenue")
plt.tight_layout()

plt.savefig(
    os.path.join(graph_folder, "spend_vs_revenue.png"),
    dpi=300
)
plt.close()

# Final output
print("\n===================================")
print("DATA VISUALIZATION COMPLETED!")
print("===================================")

print("Total graphs generated:", 5)
print("Graphs saved in:", graph_folder)

print("\nGenerated graphs:")

for file in os.listdir(graph_folder):
    if file.endswith(".png"):
        print("-", file)

print("\nAll visualization tasks completed!")
