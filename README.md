# 🌌 NEOvision: Near-Earth Object Tracker ☄️

**NEOvision** is an interactive visualization dashboard built with **Streamlit** and powered by data from **NASA JPL's SBDB Close-Approach API** combined with custom **Machine Learning predictions**. It tracks, classifies, and visualizes Near-Earth Objects (NEOs) based on their physical and orbital characteristics — helping identify potential hazards to Earth.

---

## 🚀 Features

- 🔎 **Filter and explore NEOs** by:
  - Date range of close approach
  - Distance from Earth (in AU)
  - Estimated diameter (in km)
  - Predicted hazardous status (ML output)
- 📊 **Visualizations included**:
  - 📈 Line chart of NEO diameter over time
  - ☢️ Pie chart of hazardous vs non-hazardous predictions
  - 📏 Scatter plot: Relative velocity vs Distance (colored by hazard class)
  - 📉 Histograms for distance, velocity, and diameter distributions
  - 🔄 Violin/KDE plot of diameter grouped by hazard status
  - 🧊 Correlation heatmap (distance, velocity, diameter)
  - 🧮 Binned count plots: hazard rates by binned velocity, size, and distance
  - 📅 Calendar heatmap: daily hazardous NEO frequencies
  - 🛰️ Interactive data table
  - ⏳ Live countdown to the next NEO close approach

- 🌐 Fully interactive with **Plotly**
- ⚙️ Fast and easy to run with **Streamlit**

---

## 📂 File Structure
```
NEO-EARTH-CLOSE-APPROACHES-ML/                  
├── app/
│   └── dashboard.py        # Core dashboard logic and plots
├── data/
│   ├── neos_labeled.csv    # Labeled NEO data with ML
│   ├── historical_neos.csv    # Unlabeled NEO data without ML
│   └── raw_data.json    # Raw fetched data straight from the API
├── models/
│   └── neo_classifier.pkl        # Machine Learning Model
├── notebooks/
│   ├── explorations.ipynb    # Exploratory Data Analysis
│   ├── feature_engineering.ipynb    # Feature Engineering
│   ├── historical.ipynb    # Fetching and Saving Historical Data
│   └── ml_modeling.ipynb    # ML Modeling Script
├── utils/
│   ├── fetch_data.py    # Fetching Real Time data from the API
│   ├── load_model_and_predict.py    # Model Predictions
│   ├── predict_live.py    # Real Time Prediction
│   ├── predict.py    # GridSearch Predictions
│   └── preprocess.py    # Data Preprocessing
├── requirements.txt        # Python dependencies
└── README.md               # This file
```
---

## 📊 Data Format: `neos_labeled.csv`

Your dataset should include the following columns:

| Column                 | Description                                  |
|------------------------|----------------------------------------------|
| `des`                   | Designation — Short identifier for the NEO (e.g., a number or name like 2021 PDC) |
| `orbit_id`             | Orbit ID — Identifier for the specific orbital solution or observation arc|
| `jd`                 | Julian Date — The close approach time in Julian date format |
| `cd`             | Calendar Date — Human-readable close approach datetime (e.g., 2029-04-13 21:46)|
| `dist`                | Nominal Distance — Best estimate of distance from Earth at closest approach (in AU)|
| `dist_min` | Minimum Distance — Minimum possible distance at closest approach (in AU)|
| `dist_max` | Maximum Distance — Maximum possible distance at closest approach (in AU)|
|`v_rel`| Relative Velocity — Velocity relative to Earth at closest approach (in km/s)|
|`v_inf`| Velocity Infinity — Velocity of the object at infinity (used in orbital mechanics) (km/s)|
|`t_sigma_f`| Timing Uncertainty — Uncertainty in the close-approach time (in seconds or days)|
|`h`| Absolute Magnitude — Brightness of the object; used to estimate size|
|`diameter`| Estimated Diameter — Size of the NEO in kilometers (estimated from h if not measured)|
|`diameter_sigma`| Diameter Uncertainty — Uncertainty in the diameter estimate (in km)|
|`fullname`| Full Name — Full designation of the NEO, including catalog ID|
|`days_until_approach`| Days Until Approach — Number of days from now until the close-approach date|
|`risk_level`| Risk Level (Custom) — Custom score or label indicating severity or likelihood of threat|
|`hazardous`| Hazard Label — Binary value (1 = potentially hazardous, 0 = not hazardous)|

```
AU (Astronomical Unit) ≈ 149.6 million km, which is the average distance from Earth to the Sun.

Relative Velocity (v_rel) is particularly important — high-speed NEOs can be more dangerous due to impact energy.

Absolute Magnitude (h) is used when diameter isn’t directly measured; lower h values generally indicate larger objects.

hazardous is typically defined by NASA as any object that comes within 0.05 AU and has a diameter > ~140 meters.
```

### 📁 Example:

```csv
des,orbit_id,jd,cd,dist,dist_min,dist_max,v_rel,v_inf,t_sigma_f,h,diameter,diameter_sigma,fullname,days_until_approach,risk_level,hazardous
509352,57,2415024.433789572,1900-01-04 22:25:00,0.0096318386169879,0.0096249478918661,0.00963873093215,0.20103115950940506,8.65480697513416,00:02,0.3179916317991631,,,509352 (2007 AG),-45810,close,0
```
## ▶️ Getting Started

1. Clone this repository
```
git clone https://github.com/yourusername/NEO-Earth-Close-Approaches-ML.git
cd NEO-Earth-Close-Approaches-ML
```

2. Create a Virtual Environment (Optional)
```
python -m venv env
source env/bin/activate
```

3. Install required packages
```
pip install -r requirements.txt
```

4. Launch the Streamlit dashboard
```
cd app
streamlit run dashboard.py
```

## 🤖 Machine Learning Classification

The is_hazardous_prediction column in neos_labeled.csv is produced by a custom ML model that classifies NEOs as hazardous or non-hazardous based on:
- Distance from Earth (AU)
- Relative velocity (km/s)
- Estimated diameter (km)

The model was trained using historical NASA NEO data and cross-validated for reliability.

## Future Updates

Currently, the project displays the results of our inferences made while predicting the dataset we fetched by our side, will be updating this project with a real-time classification one.

## ✨ Authors

Built with ❤️ by:
- Raif Mondal [@myselfRaifMondal](https://github.com/myselfRaifMondal)
- Syed Rafat Halim [@rafat09](https://github.com/rafat09)

🔗 Powered by:
- NASA/JPL SBDB Close-Approach API
- Custom-Trained ML classification pipeline

## 📬 Feedback & Contributions

Have suggestions, ideas, or bugs to report?
- Fork and contribute via pull request
- Open an issue for bugs or feature requests
- We’d love your feedback!


