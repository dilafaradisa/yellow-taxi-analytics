from airflow import DAG
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
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
    """Download file parquet"""
    r = requests.get(URL, stream=True)
    with open(RAW_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=10000):
            f.write(chunk)

def _transform():
    """transform data: ubah string->datetime, tambah column hari"""

    df = pd.read_parquet(RAW_FILE, engine="pyarrow")
    
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    
    df["pickup_day"] = df["tpep_pickup_datetime"].dt.day_name()
    
    df.to_parquet(TRANSFORMED_FILE, index=False)

def _load():
    """load data (parquet) ke postgres"""

    df = pd.read_parquet(TRANSFORMED_FILE, engine="pyarrow")
    engine = create_engine(POSTGRES_CONN)
    
    # Simpan ke table "yellow_taxi" (replace biar gampang coba-coba)
    # df.to_sql("yellow_taxi", engine, if_exists="replace", index=False)

    # df.to_sql("yellow_taxi", engine, if_exists="append", index=False)
    for i in range(0, len(df), 50000): 
        chunk = df.iloc[i:i+50000]
        chunk.to_sql("yellow_taxi", engine, if_exists="append", index=False)

    print("Data loaded to Postgres table: yellow_taxi")


@dag( 
	start_date = datetime(2025, 1, 1),
	schedule = '@daily',
	catchup = False, 
	tags = ['yellow_taxi', 'etl']
)

def yellow_taxi_etl():
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=_extract
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=_transform
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=_load
    )

    extract_task >> transform_task  >> load_task

yellow_taxi_etl()