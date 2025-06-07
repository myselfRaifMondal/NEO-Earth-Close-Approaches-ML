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

st.sidebar.header("Filter NEOs")
max_distance = st.sidebar.slider("Max Approach Distance (AU)", 0.0, 0.05, 0.01)
min_diameter = st.sidebar.slider("Min Diameter (km)", 0.0, 1.0, 0.1)
hazard_filter = st.sidebar.selectbox("Show Only Hazardous?", ["All", "Yes", "No"])
filtered = data[
    (data["dist"] <= max_distance) &
    (data["diameter"] >= min_diameter)
]

if hazard_filter == "Yes":
    filtered = filtered[filtered["is_hazardous_prediction"] == 1]
elif hazard_filter == "No":
    filtered = filtered[filtered["is_hazardous_prediction"] == 0]
st.metric("Total NEOs", len(filtered))
st.metric("Hazardous NEOs", filtered["is_hazardous_prediction"].sum())

st.dataframe(
    filtered[["cd", "fullname", "dist", "diameter", "v_rel", "is_hazardous_prediction"]],
    use_container_width=True
)

fig1 = px.scatter(
    filtered,
    x="cd", y="dist",
    color="is_hazardous_prediction",
    size="diameter",
    hover_name="fullname",
    labels={"cd": "Close Approach Date", "dist": "Distance (AU)", "is_hazardous_prediction": "Hazardous"}
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    filtered.sort_values("cd"),
    x="cd", y="v_rel",
    title="Relative Velocity Over Time",
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

next_cd = pd.to_datetime(filtered["cd"].iloc[0])
now = datetime.utcnow()
delta = next_cd - now
st.success(f"🕒 Next close approach in {delta.days} days and {delta.seconds // 3600} hours!")

st.markdown("---")
st.markdown("Made by Raif Mondal & Syed Rafat Halim | Powered by NASA SBDB API and ML predictions 🤖☄️")
