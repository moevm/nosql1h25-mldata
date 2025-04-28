FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache netcat-openbsd

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app

EXPOSE 5000

ENV MONGO_HOST=db
ENV MONGO_PORT=27017

ENTRYPOINT ["/bin/sh", "-c", "\
    while ! nc -z $MONGO_HOST $MONGO_PORT; do \
      sleep 1; \
    done; \
    python /app/create_db.py; \
    exec flask --app /app/run.py run  --host=0.0.0.0 --port=5000 \
"]