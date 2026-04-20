import requests
import pandas as pd

API_URL = "https://data.sfgov.org/resource/5cei-gny5.json"

def fetch_eviction_data(start_date: str):
    query_params = {
        "$where": f"file_date >= '{start_date}'",
        "$limit": 500
    }

    response = requests.get(API_URL, params=query_params)
    response.raise_for_status()

    df = pd.DataFrame(response.json())

    if not df.empty:
        df["file_date"] = pd.to_datetime(df["file_date"])

    return df