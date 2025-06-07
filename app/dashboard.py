import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# Config
st.set_page_config(page_title="NEOvision ☄️", layout="wide")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #F63366;'>🌌 NEOvision: Near-Earth Object Tracker ☄️</h1>",
    unsafe_allow_html=True
)

# Load Data
data = pd.read_csv("data/neo_predictions.csv")
data["cd"] = pd.to_datetime(data["cd"])

# Sidebar Filters
st.sidebar.header("🔍 Filter NEO Data")

min_date = data["cd"].min()
max_date = data["cd"].max()

date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

max_distance = st.sidebar.slider("Max Distance (AU)", 0.0001, 0.05, 0.01)
min_diameter = st.sidebar.slider("Min Diameter (km)", 0.0, 1.0, 0.1)
hazard_filter = st.sidebar.selectbox("Show Only Hazardous?", ["All", "Yes", "No"])
timeline_type = st.sidebar.radio("Timeline Granularity", ["Daily", "Weekly"], index=0)

# Apply filters
filtered_df = data[
    (data["cd"] >= start_date) &
    (data["cd"] <= end_date) &
    (data["dist"] <= max_distance) &
    (data["diameter"].fillna(0) >= min_diameter)
]

if hazard_filter == "Yes":
    filtered_df = filtered_df[filtered_df["is_hazardous_prediction"] == 1]
elif hazard_filter == "No":
    filtered_df = filtered_df[filtered_df["is_hazardous_prediction"] == 0]

# Metrics
st.subheader("📈 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("🪐 Total NEOs", len(filtered_df))
col2.metric("☢️ Hazardous", filtered_df["is_hazardous_prediction"].sum())
col3.metric("📅 Date Range", f"{start_date.date()} to {end_date.date()}")

# Timeline
st.subheader("📅 NEO Approaches Timeline")
timeline_data = filtered_df.copy()

if timeline_type == "Daily":
    timeline_data["date"] = timeline_data["cd"].dt.date
    timeline_count = timeline_data.groupby("date").size().reset_index(name="NEO Count")
    timeline_count["Rolling Avg"] = timeline_count["NEO Count"].rolling(window=3).mean()

    fig_timeline = px.line(
        timeline_count, x="date", y=["NEO Count", "Rolling Avg"],
        title="NEO Approaches (Daily Count vs Rolling Average)",
        markers=True,
        labels={"value": "NEO Count", "variable": "Metric"}
    )

else:
    timeline_data["week"] = timeline_data["cd"].dt.to_period("W").dt.start_time
    weekly_count = timeline_data.groupby("week").size().reset_index(name="NEO Count")
    fig_timeline = px.bar(
        weekly_count, x="week", y="NEO Count",
        title="NEO Approaches per Week",
        labels={"week": "Week", "NEO Count": "Number of Approaches"}
    )

with st.expander("📅 View NEO Timeline", expanded=True):
    st.plotly_chart(fig_timeline, use_container_width=True)

# Scatter Plot
st.subheader("📏 Distance vs Diameter")
fig_scatter = px.scatter(
    filtered_df,
    x="dist", y="diameter",
    color=filtered_df["is_hazardous_prediction"].map({1: "Hazardous", 0: "Non-Hazardous"}),
    hover_data=["fullname", "cd"],
    title="Asteroid Distance vs Diameter",
    labels={"dist": "Distance (AU)", "diameter": "Diameter (km)"}
)
with st.expander("📏 View Scatterplot", expanded=False):
    st.plotly_chart(fig_scatter, use_container_width=True)

# Pie Chart
st.subheader("🧪 Hazardous Prediction Split")
hazard_counts = filtered_df["is_hazardous_prediction"].value_counts().rename({1: "Hazardous", 0: "Non-Hazardous"}).reset_index()
hazard_counts.columns = ["Prediction", "Count"]
fig_pie = px.pie(
    hazard_counts,
    names="Prediction", values="Count",
    title="Hazardous vs Non-Hazardous NEOs",
    color="Prediction",
    color_discrete_map={"Hazardous": "crimson", "Non-Hazardous": "royalblue"}
)
with st.expander("☢️ View Prediction Distribution", expanded=False):
    st.plotly_chart(fig_pie, use_container_width=True)

# Data Table
st.subheader("🚁 Filtered NEO Data")
st.dataframe(
    filtered_df[["cd", "fullname", "dist", "diameter", "v_rel", "is_hazardous_prediction"]],
    use_container_width=True
)

# Additional Visualizations
st.subheader("📡 Close Approach Distance vs Time")
fig1 = px.scatter(
    filtered_df,
    x="cd", y="dist",
    color="is_hazardous_prediction",
    size="diameter",
    hover_name="fullname",
    labels={"cd": "Approach Date", "dist": "Distance (AU)", "is_hazardous_prediction": "Hazardous"}
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🚀 Relative Velocity Over Time")
fig2 = px.line(
    filtered_df.sort_values("cd"),
    x="cd", y="v_rel",
    title="Relative Velocity of NEOs Over Time",
    markers=True,
    labels={"cd": "Date", "v_rel": "Velocity (km/s)"}
)
st.plotly_chart(fig2, use_container_width=True)

# Countdown
if not filtered_df.empty:
    next_cd = filtered_df["cd"].iloc[0]
    now = datetime.utcnow()
    delta = next_cd - now
    st.success(f"🕒 Next close approach in {delta.days} days and {delta.seconds // 3600} hours!")

# Footer
st.markdown("---")
st.markdown("Made by **Raif Mondal** & **Syed Rafat Halim** | Powered by NASA SBDB API + ML Predictions 🤖☄️")
