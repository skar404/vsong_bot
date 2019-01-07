FROM python:3.7-slim

RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /code

CMD ["python", "manage.py", "web"]
