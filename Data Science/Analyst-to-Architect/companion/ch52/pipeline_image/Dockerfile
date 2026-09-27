# Riverstone Daily Sales Flash pipeline: a container image for the Chapter 46 Dagster job.
# Riverstone Supplies is fictional; every name and number is invented.

FROM python:3.12-slim AS base

# System packages the pipeline needs at run time (nothing here is needed only for building)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies before copying code: this layer only rebuilds when requirements.txt changes,
# not every time application code changes (Chapter 52, section 52.2's caching lesson).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code
COPY ingest.py apply_day.py make_files.py mock_crm_api.py ./
COPY dagster_definitions.py .

# Never bake secrets into an image (section 52.6): the CRM token arrives at run time.
ENV RIVERSTONE_SOURCE="dbname=riverstone_source"
ENV PYTHONUNBUFFERED=1

# Run as a non-root user: a compromised container process shouldn't have root inside the image
RUN useradd --create-home pipeline
USER pipeline

EXPOSE 3000
CMD ["dagster", "dev", "-f", "dagster_definitions.py", "-h", "0.0.0.0", "-p", "3000"]
