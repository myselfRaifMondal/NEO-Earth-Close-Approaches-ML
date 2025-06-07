# 🌌 NEOvision: Near-Earth Object Tracker ☄️

NEOvision is an interactive dashboard built with **Streamlit** and powered by **NASA JPL's SBDB Close-Approach API** + Machine Learning predictions. It visualizes and classifies near-Earth objects (NEOs) based on distance, diameter, velocity, and hazardous potential.

---

## 🚀 Features

- Filter NEOs by date, distance (AU), diameter (km), and hazard risk
- Visualize:
  - 📈 Timeline of NEO approaches
  - ☢️ Hazardous vs Non-Hazardous Pie Chart
  - 📏 Scatterplot of Distance vs Diameter
  - 🛰️ Table view of selected data
  - 🕒 Countdown to next predicted NEO
- Fully interactive using Plotly and Streamlit

---

## 📂 File Structure
NEO-EARTH-CLOSE-APPROACHES-ML
```
├── app.py # Streamlit dashboard
├── data/
│ └── neo_predictions.csv # ML predictions + NEO info
├── requirements.txt # Python dependencies
└── README.md # This file
```


---

## 📊 Data Format: `neo_predictions.csv`

Your CSV should have the following columns:

| Column | Description |
|--------|-------------|
| `cd` | Close approach date (datetime format) |
| `fullname` | Full object name (e.g., 99942 Apophis) |
| `dist` | Distance from Earth in AU |
| `diameter` | Estimated diameter in km |
| `v_rel` | Relative velocity in km/s |
| `is_hazardous_prediction` | 1 for hazardous, 0 for non-hazardous |

Example:

```csv
cd,fullname,dist,diameter,v_rel,is_hazardous_prediction
2029-04-13 21:46,99942 Apophis,0.000254,0.34,7.42,1
```
## ▶️ Run the App

pip install -r requirements.txt
streamlit run app.py

## ✨ Authors

Built by:

Raif Mondal
Syed Rafat Halim
Powered by:

NASA/JPL SBDB Close-Approach API
Your own Machine Learning Model
