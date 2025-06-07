# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="NEOvision AI 🚀", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>🤖 NEOvision AI - ML-Classified Hazardous NEOs</h1>",
    unsafe_allow_html=True
)

st.markdown("""
Welcome to **NEOvision AI**, a dashboard that simulates Machine Learning–based classification of Near-Earth Objects (NEOs) using NASA's approach data.
Here, `hazardous` is treated as a predicted label by a trained ML model.
""")

# --- Load Data ---
df = pd.read_csv("../data/neos_labeled.csv")
df["cd"] = pd.to_datetime(df["cd"])  # Convert approach date

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
st.markdown("### 🧠 Classified NEOs Overview")
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

# --- Visualizations ---
st.markdown("### 📊 Visual Insights")

# Hazard Distribution
fig1 = px.pie(filtered_df, names="hazardous", title="Hazardous vs Non-Hazardous NEOs")
st.plotly_chart(fig1, use_container_width=True)

# Velocity vs Diameter
if {"v_rel", "diameter"}.issubset(filtered_df.columns):
    fig2 = px.scatter(
        filtered_df, x="v_rel", y="diameter", color="hazardous",
        title="Velocity vs Diameter (Hazardous Coloring)",
        labels={"v_rel": "Relative Velocity (km/s)", "diameter": "Estimated Diameter (km)"},
        hover_data=["fullname", "cd"]
    )
    st.plotly_chart(fig2, use_container_width=True)

# Risk Level Distribution
if "risk_level" in filtered_df.columns:
    fig3 = px.histogram(
        filtered_df, x="risk_level", color="hazardous",
        barmode="group", title="Risk Level Distribution by Hazard Status"
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- Full Table ---
with st.expander("📚 View Full Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>🚀 Built with Streamlit & Plotly | Simulated ML Classification | Data Source: neos_labeled.csv</p>",
    unsafe_allow_html=True
)