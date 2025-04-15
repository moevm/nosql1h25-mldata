FROM python:3.11-alpine

WORKDIR /app

COPY ./app/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=5000"]