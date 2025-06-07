# utils/preprocess.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Initialize scaler (to be reused if saved during training)
scaler = MinMaxScaler()

def preprocess(df):
    # Ensure all column names are lowercase for consistency
    df.columns = [str(col).lower() for col in df.columns]

    # Convert 'cd' (close-approach date) to datetime
    if 'cd' in df.columns:
        df['cd'] = pd.to_datetime(df['cd'], errors='coerce')
        df['days_until_approach'] = (df['cd'] - pd.Timestamp.now()).dt.days
    else:
        df['days_until_approach'] = None

    # Bin distance (dist) into risk categories
    def bin_risk(dist):
        if dist < 0.01:
            return 'close'
        elif dist < 0.1:
            return 'medium'
        else:
            return 'far'

    df['risk_category'] = df['dist'].apply(bin_risk)

    # Create a binary hazard label based on dist and diameter
    df['hazardous'] = ((df['dist'] < 0.01) & (df['diameter'] > 0.15)).astype(int)

    # Fill missing values (if any) with 0 or a reasonable default
    for col in ['v_rel', 'h', 'diameter']:
        df[col] = df[col].fillna(0)

    # Normalize selected features (same scaler must be used as during training)
    try:
        df[['v_rel', 'h', 'diameter']] = scaler.fit_transform(df[['v_rel', 'h', 'diameter']])
    except:
        pass  # In case these columns are missing during inference

    return df
