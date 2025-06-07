import streamlit as st
import plotly.express as px
from datetime import datetime


st.set_page_config(page_title="NEOvision 🌍☄️", layout="wide")
st.title("🚀 NEOvision – Near-Earth Object Tracker")
st.markdown("""
Track and visualize near-Earth asteroids and comets approaching Earth, powered by [NASA SBDB API](https://ssd-api.jpl.nasa.gov/doc/cad.html) and ML predictions.  
""")

import pandas as pd

data = pd.read_csv("data/neo_predictions.csv")  # Includes ML predictions

data["cd"] = pd.to_datetime(data["cd"])

st.sidebar.header("🔍 Filter NEO Data")

# Date range
min_date = data["cd"].min()
max_date = data["cd"].max()

date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

# Distance filter (AU)
max_distance = st.sidebar.slider("Max Distance (AU)", 0.0001, 0.05, 0.01)

# Diameter filter (KM)
min_diameter = st.sidebar.slider("Min Diameter (km)", 0.0, 1.0, 0.1)

# Hazardous prediction filter
hazard_filter = st.sidebar.selectbox("Show Only Hazardous?", ["All", "Yes", "No"])

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

st.subheader("📈 Summary Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("🪐 Total NEOs", len(filtered_df))
col2.metric("☢️ Hazardous", filtered_df["is_hazardous_prediction"].sum())
col3.metric("📅 Date Range", f"{start_date.date()} to {end_date.date()}")


st.subheader("🛰️ Filtered NEO Data")
st.dataframe(
    filtered_df[["cd", "fullname", "dist", "diameter", "v_rel", "is_hazardous_prediction"]],
    use_container_width=True
)


fig1 = px.scatter(
    filtered_df,
    x="cd", y="dist",
    color="is_hazardous_prediction",
    size="diameter",
    hover_name="fullname",
    labels={"cd": "Close Approach Date", "dist": "Distance (AU)", "is_hazardous_prediction": "Hazardous"}
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    filtered_df.sort_values("cd"),
    x="cd", y="v_rel",
    title="Relative Velocity Over Time",
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

next_cd = pd.to_datetime(filtered_df["cd"].iloc[0])
now = datetime.utcnow()
delta = next_cd - now
st.success(f"🕒 Next close approach in {delta.days} days and {delta.seconds // 3600} hours!")

st.markdown("---")
st.markdown("Made by Raif Mondal & Syed Rafat Halim | Powered by NASA SBDB API and ML predictions 🤖☄️")
