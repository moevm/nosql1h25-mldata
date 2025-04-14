FROM python:3.11-alpine3.21

WORKDIR /app

COPY ./app/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./app/create_db.py .

ENTRYPOINT ["python"]
CMD ["create_db.py"]