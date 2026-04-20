# file: eviction_ingest.py
import requests
import pandas as pd
from google.cloud import storage
from io import BytesIO
import os

# --------------------------
# Config
# --------------------------
GCS_BUCKET = "eviction-data-pipeline-2026"
GCS_FOLDER = "evictions/raw/"
# API_URL = "https://data.sfgov.org/resource/eviction-notices.json"
# API_URL = "https://data.sfgov.org/api/v3/views/5cei-gny5/query.json"
API_URL = "https://data.sfgov.org/resource/5cei-gny5.json"
START_DATE = "2026-01-01"

# --------------------------
# Step 1: Data Preparation
# --------------------------
def fetch_eviction_data(start_date=START_DATE):
    query_params = {
        "$where": f"file_date >= '{start_date}'",
        "$limit": 50
    }
    response = requests.get(API_URL, params=query_params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    
    if not df.empty:
        df["file_date"] = pd.to_datetime(df["file_date"])
    return df

# --------------------------
# Step 2: Upload to GCS
# --------------------------
def upload_to_gcs(df, bucket_name=GCS_BUCKET, folder=GCS_FOLDER):
    """
    Save the dataframe as Parquet to GCS
    Partition by file_date
    """
    if df.empty:
        print("No data to upload")
        return
    
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    # 按 file_date 存檔
    for file_date, group in df.groupby(df["file_date"].dt.date):
        file_name = f"{folder}file_date={file_date}/evictions.parquet"
        buf = BytesIO()
        group.to_parquet(buf, index=False)
        blob = bucket.blob(file_name)
        blob.upload_from_string(buf.getvalue(), content_type="application/octet-stream")
        print(f"Uploaded {len(group)} rows to {file_name}")

# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    df = fetch_eviction_data()
    print(df.head())
    upload_to_gcs(df)


# pip install pandas requests pyarrow google-cloud-storage
# export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"