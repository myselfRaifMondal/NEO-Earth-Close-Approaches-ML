import requests
import pandas as pd
from datetime import datetime, timedelta
import joblib

# 1. Fetch data
today = datetime.now().strftime('%Y-%m-%d')
end_date = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')

params = {
    'body': 'Earth',
    'date-min': today,
    'date-max': end_date,
    'neo': 'true',
    'diameter': 'true',
    'fullname': 'true'
}

response = requests.get('https://ssd-api.jpl.nasa.gov/cad.api', params=params)
data = response.json()

# 2. Convert and preprocess (similar steps as before)
df = pd.json_normalize(data['data'], sep='_')
# Rename columns, parse dates, handle missing, create features, normalize etc.

# 3. Load model
model = joblib.load('models/neo_classifier.pkl')

# 4. Predict hazard
X_new = df[feature_columns]  # make sure features are in correct order
predictions = model.predict(X_new)
df['hazardous'] = predictions

# 5. Save results
df.to_csv('data/upcoming_neo_predictions.csv', index=False)
