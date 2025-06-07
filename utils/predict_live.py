# utils/predict_live.py

import pandas as pd
import joblib
import requests
from preprocess import preprocess  # Make sure preprocess.py exists in utils/

# Load the trained model
model = joblib.load("models/neo_classifier.pkl")

# Set API endpoint and parameters
url = "https://ssd-api.jpl.nasa.gov/cad.api"
params = {
    "body": "Earth",
    "date-min": "now",
    "date-max": "2100-01-01",
    "dist-max": "0.5",  # Only show reasonably close approaches
    "diameter": "true",
    "fullname": "true",
    "neo": "true",
    "sort": "date",
    "limit": "50"
}

response = requests.get(url, params=params)
data = response.json()

# Convert JSON to DataFrame
cols = data['fields']
df = pd.DataFrame(data['data'], columns=cols)

# Rename for convenience and numeric conversion
numeric_cols = ['dist', 'v_rel', 'v_inf', 'diameter', 'h']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Preprocess data
processed_df = preprocess(df.copy())

# Select features for prediction (ensure same as during training)
feature_columns = ['v_rel', 'h', 'diameter', 'days_until_approach']
X_new = processed_df[feature_columns]

# Predict hazard
predictions = model.predict(X_new)
processed_df['hazard_prediction'] = predictions

# Display the top predicted hazardous NEOs
print("\n🔍 Predicted Hazardous NEOs (Next 50 Approaches):")
print(processed_df[['des', 'cd', 'dist', 'diameter', 'hazard_prediction']].head(10))
