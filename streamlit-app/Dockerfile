FROM python:3.9-slim

# Install build tools and runtime libraries for numpy/pandas on ARM
RUN apt-get update && apt-get install -y build-essential libatlas3-base

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir streamlit pandas sqlalchemy psycopg2-binary

EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]