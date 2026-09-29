FROM python:3.14-slim

RUN useradd --create-home pipeline

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingest.py riverstone_pipeline.py run_flash.py ./
RUN mkdir warehouse exports outbox alerts /home/pipeline/dagster_home \
    && chown pipeline warehouse exports outbox alerts /home/pipeline/dagster_home

ENV PYTHONUNBUFFERED=1
ENV DAGSTER_HOME=/home/pipeline/dagster_home
ENV RIVERSTONE_SOURCE="dbname=riverstone_source"

USER pipeline

CMD ["python", "run_flash.py"]
