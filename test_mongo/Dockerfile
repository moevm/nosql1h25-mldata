FROM python:3.11-slim

WORKDIR /test_mongo

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY . .

ENTRYPOINT ["pytest", "-s"]
CMD ["test_mongo.py"]