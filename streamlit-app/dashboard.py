import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# --------------------------------------------
# 1️⃣ KONFIGURASI DATABASE
# --------------------------------------------
DB_HOST = "localhost"      # kalau Streamlit jalan di host
DB_PORT = "5433"
DB_NAME = "airflow"
DB_USER = "airflow"
DB_PASS = "airflow"

# Buat koneksi ke Postgres
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# --------------------------------------------
# 2️⃣ LOAD DATA
# --------------------------------------------
@st.cache_data
def load_data():
    query = """
    SELECT 
        tpep_pickup_datetime AS pickup_time,
        tpep_dropoff_datetime AS dropoff_time,
        passenger_count,
        trip_distance,
        total_amount
    FROM yellow_taxi
    LIMIT 5000;
    """
    return pd.read_sql(query, engine)

st.title("🚖 Yellow Taxi Analytics Dashboard")
st.caption("Data sample dari PostgreSQL (via Airflow pipeline)")

df = load_data()

# --------------------------------------------
# 3️⃣ TAMPILKAN DATAFRAME
# --------------------------------------------
st.subheader("Raw Data Preview")
st.dataframe(df.head())

# --------------------------------------------
# 4️⃣ VISUALISASI SEDERHANA
# --------------------------------------------
st.subheader("📈 Distribusi Trip Distance")
st.line_chart(df["trip_distance"])

st.subheader("💰 Total Amount Distribution")
st.bar_chart(df["total_amount"])

# --------------------------------------------
# 5️⃣ AGGREGASI PER HARI (jika kolom datetime ada)
# --------------------------------------------
df["pickup_date"] = pd.to_datetime(df["pickup_time"]).dt.date
daily = df.groupby("pickup_date")["total_amount"].sum().reset_index()

st.subheader("📅 Total Amount per Hari")
st.line_chart(daily.set_index("pickup_date"))
