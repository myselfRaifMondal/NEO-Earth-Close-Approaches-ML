# utils/fetch_data.py

import requests
import pandas as pd

def fetch_neo_data(start_date, end_date):
    params = {
        'body': 'Earth',
        'date-min': start_date,
        'date-max': end_date,
        'neo': 'true',
        'diameter': 'true',
        'fullname': 'true'
    }
    url = 'https://ssd-api.jpl.nasa.gov/cad.api'
    response = requests.get(url, params=params)
    data = response.json()
    
    # Use fields key for column names
    columns = data['fields']  # list of strings
    df = pd.DataFrame(data['data'], columns=columns)
    
    return df
# utils/predict.py (snippet)

def preprocess(df):
    # Make sure columns are strings and lowercase
    df.columns = [col.lower() for col in df.columns]

    # Continue with your preprocessing code, e.g.
    # convert date column to datetime
    df['cd'] = pd.to_datetime(df['cd'], errors='coerce')

    # Feature engineering, etc.

    return df


if __name__ == "__main__":
    # Example usage
    from fetch_data import fetch_neo_data

    df = fetch_neo_data('1900-01-01', '2100-01-01')
    df = preprocess(df)
    
    # continue with prediction logic...

