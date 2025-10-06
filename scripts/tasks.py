from datetime import datetime
import pandas as pd
import requests
import os
from sqlalchemy import create_engine

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"
DATA_DIR = "/opt/airflow/data"
os.makedirs(DATA_DIR, exist_ok=True)
RAW_FILE = os.path.join(DATA_DIR, "yellow_2025-01.parquet")
TRANSFORMED_FILE = os.path.join(DATA_DIR, "yellow_2025-01-transformed.csv")
POSTGRES_CONN = "postgresql://airflow:airflow@postgres:5432/airflow"

def _extract():
    """Download file parquet dari source"""
    print("📥 Downloading data...")
    r = requests.get(URL, stream=True)
    with open(RAW_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ File saved to {RAW_FILE}")

def _transform():
    """Baca parquet, ubah datetime string -> datetime, tambah column hari"""
    print("⚙️ Transforming data...")
    df = pd.read_parquet(RAW_FILE, engine="pyarrow")
    
    # Misalnya ambil pickup datetime
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    
    # Tambah kolom hari transaksi
    df["pickup_day"] = df["tpep_pickup_datetime"].dt.day_name()
    
    # Simpan ke CSV sementara
    df.to_csv(TRANSFORMED_FILE, index=False)
    print(f"✅ Transformed file saved to {TRANSFORMED_FILE}")

def _load():
    """Load data ke Postgres"""
    print("📤 Loading data to Postgres...")
    df = pd.read_csv(TRANSFORMED_FILE)
    engine = create_engine(POSTGRES_CONN)
    
    # Simpan ke table "yellow_taxi" (replace biar gampang coba-coba)
    df.to_sql("yellow_taxi", engine, if_exists="replace", index=False)
    print("✅ Data loaded to Postgres table: yellow_taxi")