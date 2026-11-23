
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Digital Marketing Analytics",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------
# PROJECT PATHS
# ----------------------------------

base_folder = r"C:\Digital_Marketing_Analytics"
data_folder = os.path.join(base_folder, "visualizations")

# ----------------------------------
# LOAD DATASETS
# ----------------------------------

@st.cache_data
def load_data():

    metrics = pd.read_csv(
        os.path.join(data_folder, "marketing_metrics.csv")
    )

    channels = pd.read_csv(
        os.path.join(data_folder, "channel_performance.csv")
    )

    campaigns = pd.read_csv(
        os.path.join(data_folder, "campaign_performance.csv")
    )

    return metrics, channels, campaigns


try:
    metrics_df, channel_df, campaign_df = load_data()

except Exception as e:
    st.error(f"Unable to load dashboard data: {e}")
    st.info("Run data_cleaning.py and marketing_analysis.py first.")
    st.stop()


# ----------------------------------
# DASHBOARD TITLE
# ----------------------------------

st.title(
    "📊 Digital Marketing Analytics: Measuring Campaign Performance"
)

st.write(
    "Analyzing Digital Marketing Campaign Effectiveness"
)

st.divider()


# ----------------------------------
# SIDEBAR FILTER
# ----------------------------------

st.sidebar.header("Dashboard Filters")

available_channels = sorted(
    metrics_df["channel"].dropna().unique().tolist()
)

selected_channels = st.sidebar.multiselect(
    "Select Marketing Channels",
    options=available_channels,
    default=available_channels
)

# Filter datasets
filtered_df = metrics_df[
    metrics_df["channel"].isin(selected_channels)
]

filtered_channels = channel_df[
    channel_df["channel"].isin(selected_channels)
]

filtered_campaigns = campaign_df[
    campaign_df["channel"].isin(selected_channels)
]

if filtered_df.empty:
    st.warning("Please select at least one marketing channel.")
    st.stop()


# ----------------------------------
# CALCULATE OVERALL METRICS
# ----------------------------------

total_impressions = filtered_df["impressions"].sum()
total_clicks = filtered_df["clicks"].sum()
total_spend = filtered_df["spend"].sum()
total_conversions = filtered_df["conversions"].sum()
total_revenue = filtered_df["revenue"].sum()

ctr = (
    total_clicks / total_impressions * 100
    if total_impressions > 0 else 0
)

cpc = (
    total_spend / total_clicks
    if total_clicks > 0 else 0
)

conversion_rate = (
    total_conversions / total_clicks * 100
    if total_clicks > 0 else 0
)

cpa = (
    total_spend / total_conversions
    if total_conversions > 0 else 0
)

roas = (
    total_revenue / total_spend
    if total_spend > 0 else 0
)


# ----------------------------------
# KPI SECTION
# ----------------------------------

st.header("Overall Marketing Performance")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Impressions",
    f"{total_impressions:,.0f}"
)

col2.metric(
    "Total Clicks",
    f"{total_clicks:,.0f}"
)

col3.metric(
    "Total Spend",
    f"{total_spend:,.2f}"
)

col4.metric(
    "Total Conversions",
    f"{total_conversions:,.0f}"
)

col5.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

col6, col7, col8, col9, col10 = st.columns(5)

col6.metric("CTR", f"{ctr:.2f}%")
col7.metric("CPC", f"{cpc:.2f}")
col8.metric("Conversion Rate", f"{conversion_rate:.2f}%")
col9.metric("CPA", f"{cpa:.2f}")
col10.metric("ROAS", f"{roas:.2f}")

st.divider()


# ----------------------------------
# BEST PERFORMING CHANNEL
# ----------------------------------

st.header("Best Performing Channel")

if not filtered_channels.empty:

    best_channel = filtered_channels.loc[
        filtered_channels["ROAS"].idxmax()
    ]

    st.success(
        f"Best Channel: {best_channel['channel']} | "
        f"ROAS: {best_channel['ROAS']:.2f}"
    )


# ----------------------------------
# BEST PERFORMING CAMPAIGN
# ----------------------------------

st.header("Best Performing Campaign")

campaign_summary = filtered_campaigns.groupby(
    "campaign", as_index=False
).agg({
    "spend": "sum",
    "revenue": "sum",
    "conversions": "sum"
})

if not campaign_summary.empty:

    campaign_summary["ROAS"] = (
        campaign_summary["revenue"] /
        campaign_summary["spend"].where(
            campaign_summary["spend"] > 0, 1
        )
    )

    campaign_summary.loc[
        campaign_summary["spend"] <= 0, "ROAS"
    ] = 0

    best_campaign = campaign_summary.loc[
        campaign_summary["ROAS"].idxmax()
    ]

    st.success(
        f"Best Campaign: {best_campaign['campaign']} | "
        f"ROAS: {best_campaign['ROAS']:.2f}"
    )


st.divider()


# ----------------------------------
# CHANNEL PERFORMANCE
# ----------------------------------

st.header("Channel-wise Performance")

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        filtered_channels,
        x="channel",
        y="revenue",
        title="Revenue by Marketing Channel",
        text_auto=".2s"
    )

    st.plotly_chart(fig, width="stretch")

with col2:

    fig = px.bar(
        filtered_channels,
        x="channel",
        y="ROAS",
        title="Return on Ad Spend by Channel",
        text_auto=".2f"
    )

    st.plotly_chart(fig, width="stretch")


# ----------------------------------
# CAMPAIGN PERFORMANCE
# ----------------------------------

st.header("Campaign-wise Performance")

campaign_revenue = campaign_summary.sort_values(
    "revenue", ascending=False
)

campaign_conversions = campaign_summary.sort_values(
    "conversions", ascending=False
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        campaign_revenue,
        x="campaign",
        y="revenue",
        title="Campaign Revenue Comparison"
    )

    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, width="stretch")

with col2:

    fig = px.bar(
        campaign_conversions,
        x="campaign",
        y="conversions",
        title="Campaign Conversion Comparison"
    )

    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, width="stretch")


# ----------------------------------
# MARKETING SPEND VS REVENUE
# ----------------------------------

st.header("Marketing Spend vs Revenue")

fig = px.scatter(
    filtered_df,
    x="spend",
    y="revenue",
    color="channel",
    hover_data=["campaign"],
    title="Marketing Spend vs Revenue"
)

st.plotly_chart(fig, width="stretch")


# ----------------------------------
# DETAILED CHANNEL TABLE
# ----------------------------------

st.header("Detailed Channel Performance")

st.dataframe(
    filtered_channels.round(2),
    width="stretch",
    hide_index=True
)


# ----------------------------------
# DETAILED CAMPAIGN TABLE
# ----------------------------------

st.header("Detailed Campaign Performance")

st.dataframe(
    filtered_campaigns.round(2),
    width="stretch",
    hide_index=True
)


# ----------------------------------
# FOOTER
# ----------------------------------

st.divider()

st.success("Dashboard loaded successfully!")

st.caption(
    "Digital Marketing Analytics: Measuring Campaign Performance"
)
