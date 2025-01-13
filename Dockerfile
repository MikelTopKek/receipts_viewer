FROM python:3.11-slim

ENV POETRY_VERSION=1.4.2

RUN pip install "poetry==$POETRY_VERSION"

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