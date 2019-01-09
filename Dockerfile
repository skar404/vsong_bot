FROM python:3.7-slim

RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . /code

EXPOSE 8080

CMD ["python", "manage.py", "web"]
