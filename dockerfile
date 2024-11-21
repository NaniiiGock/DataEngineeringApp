FROM python:3.9-slim

ENV PORT 8501
ENV PYTHONUNBUFFERED True

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x wait-for-postgres.sh

EXPOSE 8501

CMD ["./wait-for-postgres.sh", "db", "streamlit", "run", "app_with_db.py", "--server.port=8501", "--server.address=0.0.0.0"]
