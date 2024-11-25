FROM bitnami/spark:3.3.0

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "spark_consumer.py"] 