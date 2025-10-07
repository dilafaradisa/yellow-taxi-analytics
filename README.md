# Yellow Taxi Analytics

A data engineering project to analyze NYC Yellow Taxi trip data using Airflow, PostgreSQL, and Streamlit—all orchestrated with Docker Compose.

Yellow Taxi Trip Records could download from: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

ps: you need to convert from .parquet to .csv in order to make this work

This project is designed to work on:
- **Linux (x86_64 and ARM, including Armbian)**
- **macOS (Intel and Apple Silicon/M1/M2)**
- **Windows (with Docker Desktop)**

---

## **Project Structure**

- **dags/**: Airflow DAGs for ETL pipeline
- **data/**: Data files (CSV, Parquet, etc.)
- **pgdata/**: PostgreSQL data (persisted volume)
- **scripts/**: Helper scripts
- **streamlit-app/**: Streamlit dashboard app
- **docker-compose.yml**: Multi-service orchestration

---

## **Architecture & Flow**

1. **Airflow** orchestrates ETL jobs to load and transform Yellow Taxi data into PostgreSQL.
2. **PostgreSQL** stores the processed data (table: `yellow_taxi`).
3. **Streamlit** connects to PostgreSQL and visualizes the data in a web dashboard.

All services run in containers and communicate via Docker Compose's internal network.

---

## **How to Run**

### **Prerequisites**
- Docker & Docker Compose installed
- (Optional) Git to clone the repo

### **Steps**

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/yellow-taxi-analytics.git
   cd yellow-taxi-analytics
   ```

2. **Start all services**
   ```sh
   docker-compose up --build
   ```
   This will:
   - Start PostgreSQL on port **5432**
   - Start Airflow on port **8080** ([http://localhost:8080](http://localhost:8080))
   - Start Streamlit dashboard on port **8501** ([http://localhost:8501](http://localhost:8501))

3. **Stop all services**
   ```sh
   docker-compose down
   ```

---

## **Configuration**

- Database credentials and ports are set in `docker-compose.yml` and used by all services.
- To connect to PostgreSQL from your host, use:
  - Host: `localhost`
  - Port: `5432`
  - User: `airflow`
  - Password: `airflow`
  - Database: `airflow`

---

## **Notes**

- All data and database state are persisted in the `pgdata/` folder.
- If you run on ARM (e.g., Armbian), the setup uses compatible images and dependencies.
- The Streamlit app connects to the database using the Docker Compose service name (`postgres`).

---

## **Troubleshooting**

- If you get port conflicts, change the host port in `docker-compose.yml`.
- If you update dependencies, rebuild with `docker-compose up --build`.
- For ARM servers, a custom Dockerfile is used for Streamlit to ensure compatibility.
- docker.errors.DockerException: Error while fetching server API version: Not supported URL scheme http+docker:
```sh
#Uninstall the pip version of docker-compose:
pip uninstall docker-compose
pip3 uninstall docker-compose

# Use the Docker Compose plugin (recommended for modern Docker): Check if you have the new plugin:
docker compose version

# If this work, use:
docker compose up --build 

# If you need to install the plugin:
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Then use:
docker compose up --build
```