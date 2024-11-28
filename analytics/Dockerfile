FROM python:3.13.0-alpine3.20

WORKDIR /lytics

COPY analytics.py /lytics

RUN pip install --no-cache-dir Flask Pandas requests

EXPOSE 5001

ENV FLASK_APP=analytics.py

CMD ["flask", "run", "--host=127.0.0.1"]
