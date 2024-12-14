FROM python:3.13-slim

WORKDIR /serving

RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask pandas requests duckdb

EXPOSE 5001

ENV FLASK_APP=service_api.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
