# dashboard.py

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(page_title="NEOvision ☄️", layout="wide")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #F63366;'>🌌 NEOvision: Near-Earth Object Tracker ☄️</h1>",
    unsafe_allow_html=True
)

# Load Data
data = pd.read_csv("../data/neos_labeled.csv")

# Convert 'cd' (close-approach date) to datetime
data["cd"] = pd.to_datetime(data["cd"])

# Sidebar Filters
st.sidebar.header("🔍 Filter NEO Data")

# Date Range Filter
min_date = data["cd"].min()
max_date = data["cd"].max()

date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

# Filter data based on date range
data = data[(data["cd"] >= start_date) & (data["cd"] <= end_date)]

# Distance Filter
max_distance = st.sidebar.slider("Max Distance (AU)", float(data["dist"].min()), float(data["dist"].max()), 0.05)
data = data[data["dist"] <= max_distance]

# Diameter Filter
min_diameter = st.sidebar.slider("Min Diameter (km)", float(data["diameter"].min()), float(data["diameter"].max()), 0.1)
data = data[data["diameter"] >= min_diameter]

# Hazardous Filter
hazard_filter = st.sidebar.selectbox("Show Only Hazardous?", ["All", "Yes", "No"])
if hazard_filter == "Yes":
    data = data[data["hazardous"] == True]
elif hazard_filter == "No":
    data = data[data["hazardous"] == False]

# Column Selector
st.markdown("### 📋 View Custom Columns")
columns_to_display = st.multiselect("Select columns to display", options=data.columns, default=data.columns)
st.dataframe(data[columns_to_display], use_container_width=True)

# Charts Section
st.markdown("### 📊 Key Visualizations")

col1, col2 = st.columns(2)

# Risk Level Distribution
with col1:
    if "risk_level" in data.columns:
        fig_risk = px.histogram(data, x="risk_level", title="Risk Level Distribution", color="risk_level")
        st.plotly_chart(fig_risk, use_container_width=True)

# Velocity vs Diameter Scatter
with col2:
    if {"v_rel", "diameter"}.issubset(data.columns):
        fig_vel_dia = px.scatter(data, x="v_rel", y="diameter", color="risk_level",
                                 title="Relative Velocity vs Diameter", hover_data=["fullname"])
        st.plotly_chart(fig_vel_dia, use_container_width=True)

# Timeline of Approaches
if "cd" in data.columns:
    st.markdown("### 📆 NEO Timeline")
    data["date_only"] = data["cd"].dt.date
    timeline = data.groupby("date_only").size().reset_index(name="count")
    fig_timeline = px.line(timeline, x="date_only", y="count", title="Number of NEO Approaches Over Time")
    st.plotly_chart(fig_timeline, use_container_width=True)

# Expandable Full Data Viewer
with st.expander("🔎 View Full NEO Dataset"):
    st.dataframe(data, use_container_width=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Made with ❤️ using Streamlit and Plotly | Dataset: NEOs Labeled CSV", unsafe_allow_html=True)