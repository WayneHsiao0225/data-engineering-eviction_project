# 🏠 Eviction Data Engineering Project

**End-to-End Data Pipeline with dbt & Streamlit Dashboard**

---

## 📌 Problem Description

Housing instability and eviction trends are critical indicators of economic stress in urban areas. However, raw eviction datasets are often fragmented, unstructured, and not analysis-ready.

This project aims to:

- Build a scalable end-to-end data pipeline
- Transform raw eviction data into analytics-ready datasets
- Provide an interactive dashboard to explore:
  - Distribution of eviction cases
  - Temporal trends over time

👉 The final goal is to enable data-driven insights into eviction patterns for policy analysis and urban planning.

---

## 🏗️ Architecture Overview
        ┌──────────────┐
        │  External API│
        └──────┬───────┘
               │
       (Batch Ingestion)
               │
        ┌──────▼───────┐
        │   Python ETL │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  Data Lake   │ (GCS Bucket)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ Data Warehouse│ (BigQuery)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  dbt Models  │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  Streamlit   │
        │  Dashboard   │
        └──────────────┘

---

## ⚙️ Technology Stack

| Layer | Tools |
|------|------|
| Cloud | GCP (Google Cloud Storage, BigQuery) |
| Orchestration | Apache Airflow (Dockerized) |
| Data Lake | GCS |
| Data Warehouse | BigQuery |
| Transformation | dbt (Data Build Tool) |
| Processing | Python (Pandas) |
| Visualization | Streamlit |
| Containerization | Docker Compose |

---

## 🔄 Data Pipeline Design

### ✔️ Pipeline Type: Batch Processing

- Runs periodically via Airflow DAG  
- Suitable for:
  - Public datasets  
  - Non-real-time analytics  

---

### 1️⃣ Data Ingestion (Python + Airflow)

- Fetch eviction dataset via API  
- Perform initial cleaning  
- Upload raw data to GCS Data Lake  

**Features:**

- Error handling (API failure safe)  
- Modular ingestion script  
- Orchestrated via Airflow DAG  

---

### 2️⃣ Data Lake → Data Warehouse

- Load data from GCS into BigQuery  
- Use structured schema  

**Optimization:**

- Partitioned by date  
- Enables efficient time-series queries  

---

### 3️⃣ Data Transformation (dbt)

dbt is used to transform raw data into analytics-ready tables.

**dbt Models:**

- `staging_evictions`  
  - Clean raw fields  
  - Standardize column names  

- `fact_evictions`  
  - Aggregated eviction metrics  

- `dim_location`  
  - Location-based grouping  

**Features:**

- Modular SQL transformations  
- Version-controlled data models  
- Reproducible pipeline  

---

## 📊 Dashboard (Streamlit)

The dashboard includes at least two required visualizations:

### 📈 1. Categorical Distribution

- Example: Evictions by location / category  
- Insight: Identify high-risk regions  

### 📉 2. Temporal Trend

- Example: Evictions over time (daily / monthly)  
- Insight: Detect spikes and trends  

---

## 🧠 Additional Features

- Interactive filtering  
- Clean UI for exploration  
- Real-time query from BigQuery  

---

## 🚀 How to Run the Project (Reproducibility)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/WayneHsiao0225/data-engineering-eviction_project.git
cd data-engineering-eviction_project
### 2️⃣ Setup Environment Variables
# Create a .env file in the root directory
GCP_PROJECT_ID=your_project
GCS_BUCKET=your_bucket
BIGQUERY_DATASET=your_dataset

### 3️⃣ Run with Docker
docker compose up --build

### 4️⃣ Airflow
# Access UI: http://localhost:8080
# Trigger DAG:
# ingestion
# warehouse_load
# dbt_transformation

### 5️⃣ Run dbt
dbt deps
dbt run

### 6️⃣ Launch Dashboard
streamlit run app.py
