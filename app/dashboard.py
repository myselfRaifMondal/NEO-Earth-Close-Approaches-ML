# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import numpy as np

# --- Page Setup ---
st.set_page_config(page_title="NEOvision AI", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>NEOvision AI - ML-Classified Hazardous NEOs</h1>",
    unsafe_allow_html=True
)

st.markdown("""
Welcome to **NEOvision AI**, a dashboard that simulates Machine Learning–based classification of Near-Earth Objects (NEOs) using NASA's approach data.
Here, `hazardous` is treated as a predicted label by a trained ML model.
""")

# --- Load Data ---
df = pd.read_csv("../data/neos_labeled.csv")
df["cd"] = pd.to_datetime(df["cd"])

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

# Date Filter
date_range = st.sidebar.date_input(
    "Approach Date Range",
    [df["cd"].min(), df["cd"].max()]
)
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
filtered_df = df[(df["cd"] >= start_date) & (df["cd"] <= end_date)]

# Hazard Filter
hazard_filter = st.sidebar.selectbox(
    "Filter by Hazard Status",
    ["All", "Hazardous", "Not Hazardous"]
)

if hazard_filter == "Hazardous":
    filtered_df = filtered_df[filtered_df["hazardous"] == True]
elif hazard_filter == "Not Hazardous":
    filtered_df = filtered_df[filtered_df["hazardous"] == False]

# --- Overview ---
st.markdown("### Classified NEOs Overview")
st.dataframe(filtered_df.head(50), use_container_width=True)

# --- Metrics ---
total_neos = len(filtered_df)
haz_count = filtered_df["hazardous"].sum()
nonhaz_count = total_neos - haz_count
haz_pct = (haz_count / total_neos) * 100 if total_neos > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("☄️ Total NEOs", total_neos)
col2.metric("🚨 Hazardous", haz_count)
col3.metric("🟢 % Hazardous", f"{haz_pct:.2f}%")

# --- Visual Insights ---
st.markdown("### Visual Insights")

# 📈 Line Chart: cd vs diameter
line_df = filtered_df.sort_values("cd")
fig_line = px.line(line_df, x="cd", y="diameter", title="NEO Diameters Over Time")
st.plotly_chart(fig_line, use_container_width=True)

# 📊 Histogram: dist, v_rel, diameter
st.markdown("#### Histograms of Key Features")
cols = st.columns(3)
for col, feat in zip(cols, ["dist", "v_rel", "diameter"]):
    with col:
        fig = px.histogram(filtered_df, x=feat, nbins=40, title=f"Distribution of {feat}")
        st.plotly_chart(fig, use_container_width=True)

# 🔵 Scatter Plot: v_rel vs dist colored by hazardous
fig_scatter = px.scatter(
    filtered_df, x="v_rel", y="dist", color="hazardous",
    title="Velocity vs Distance Colored by Hazard Status",
    labels={"v_rel": "Relative Velocity (km/s)", "dist": "Miss Distance (LD)"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

# 🧊 Correlation Heatmap
st.markdown("#### Correlation Heatmap")
corr = filtered_df[["v_rel", "dist", "diameter"]].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# 🔄 KDE/Violin Plot
st.markdown("#### Diameter Distribution by Hazard Status")
fig_violin = px.violin(filtered_df, y="diameter", x="hazardous", box=True, points="all",
                       title="Diameter Distribution by Hazard Status")
st.plotly_chart(fig_violin, use_container_width=True)

# ⚠️ Risk Level vs Hazardous (if 'risk_level' exists)
if "risk_level" in filtered_df.columns:
    fig_risk = px.histogram(filtered_df, x="risk_level", color="hazardous",
                            title="Risk Level by Hazardous Classification", barmode="group")
    st.plotly_chart(fig_risk, use_container_width=True)

# 🧮 Count Plot: hazardous by bins of dist, v_rel, diameter
st.markdown("#### Hazard Count by Binned Features")
for feature in ["dist", "v_rel", "diameter"]:
    binned = pd.cut(filtered_df[feature], bins=5)
    filtered_df[f"{feature}_bin"] = binned.astype(str)
    fig_count = px.histogram(
        filtered_df, x=f"{feature}_bin", color="hazardous",
        title=f"Hazard Status by {feature.capitalize()} Bins", barmode="group"
    )
    st.plotly_chart(fig_count, use_container_width=True)

# 📅 Calendar Heatmap of hazardous count per day
st.markdown("#### Calendar Heatmap of Hazardous NEO Approaches")
haz_df = filtered_df[filtered_df["hazardous"] == True]
haz_df["date"] = haz_df["cd"].dt.date
haz_df["day"] = haz_df["cd"].dt.day
haz_df["month"] = haz_df["cd"].dt.month_name().str[:3]

# Group to remove duplicates
heatmap_data = (
    haz_df.groupby(["month", "day"])
    .size()
    .reset_index(name="count")
    .pivot(index="month", columns="day", values="count")
)
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
heatmap_data = heatmap_data.reindex(month_order)
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(heatmap_data, cmap="Reds", linewidths=0.5, linecolor='gray', annot=True, fmt=".0f")
plt.title("Hazardous NEO Counts by Date")
st.pyplot(fig)