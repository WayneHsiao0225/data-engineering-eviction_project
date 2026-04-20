from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
from google.cloud import storage
from io import BytesIO

# --------------------------
# Config
# --------------------------
GCS_BUCKET = "eviction-data-pipeline-2026"
GCS_FOLDER = "evictions/raw/"
API_URL = "https://data.sfgov.org/resource/5cei-gny5.json"
START_DATE = "2026-01-01"

# --------------------------
# Step 1: Fetch
# --------------------------
def fetch_eviction_data(**context):
    params = {
        "$where": f"file_date >= '{START_DATE}'",
        "$limit": 1000
    }

    r = requests.get(API_URL, params=params, timeout=60)
    r.raise_for_status()

    df = pd.DataFrame(r.json())

    if not df.empty:
        df["file_date"] = pd.to_datetime(df["file_date"])

    # Airflow XCom（簡單傳 dict）
    return df.to_json()

# --------------------------
# Step 2: Upload to GCS
# --------------------------
def upload_to_gcs(**context):
    import json

    ti = context["ti"]
    df_json = ti.xcom_pull(task_ids="fetch_data")
    df = pd.read_json(df_json)

    if df.empty:
        print("No data to upload")
        return

    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)

    for file_date, group in df.groupby(df["file_date"].dt.date):
        file_path = f"{GCS_FOLDER}file_date={file_date}/evictions.parquet"

        buf = BytesIO()
        group.to_parquet(buf, index=False)
        buf.seek(0)  # ⚠️ important fix

        blob = bucket.blob(file_path)
        blob.upload_from_file(buf, content_type="application/octet-stream")

        print(f"Uploaded {len(group)} rows -> {file_path}")

# --------------------------
# DAG
# --------------------------
with DAG(
    dag_id="eviction_ingestion_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["gcp", "ingestion"],
) as dag:

    t1 = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_eviction_data,
    )

    t2 = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
    )

    t1 >> t2