import requests
import pandas as pd
import json
import os

def fetch_neo_data(start_date='1900-01-01', end_date='2100-01-01', save_dir='data/'):
    url = "https://ssd-api.jpl.nasa.gov/cad.api"
    params = {
        "body": "Earth",
        "neo": "true",
        "diameter": "true",
        "fullname": "true",
        "date-min": start_date,
        "date-max": end_date,
        "sort": "date",
        "limit": 100000  # You can adjust this if the API restricts it
    }

    # Call API
    response = requests.get(url, params=params)
    data = response.json()
    
    
    # Ensure directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Save raw JSON
    with open(os.path.join(save_dir, 'raw_data.json'), 'w') as f:
        json.dump(data, f, indent=4)

    # Convert to CSV
    df = pd.DataFrame(data['data'], columns=data['fields'])
    df.to_csv(os.path.join(save_dir, 'historical_neos.csv'), index=False)
    print(f"Data saved to {save_dir}historical_neos.csv")

    return df
