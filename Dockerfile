FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry cache clear --all pypi && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-ansi

RUN git config --global --add safe.directory /app

COPY ./ ./
