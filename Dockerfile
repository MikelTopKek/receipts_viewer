FROM python:3.11-slim

RUN pip install "poetry==1.7.1"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME=/usr/local/poetry \
    PATH="/usr/local/poetry/bin:$PATH"

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    python3-dev \
    libpq-dev \
    gcc \
    git \
    curl \
    unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry cache clear --all pypi && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-ansi

COPY ./ ./