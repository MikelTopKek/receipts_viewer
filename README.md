# receipts_viewer
The test task is to develop a REST API for creating and viewing checks with user registration and authorization.

## Prerequisites

- Python 3.11
- poetry

## Installation

### 1. Clone the repository via ssh:
```
git clone git@github.com:MikelTopKek/receipts_viewer.git
```

### 2. Create and activate the virtual environment.

### 3. Install dependencies:
```
pip install poetry
```
```
poetry install --all-extras
```
### 4. Generate .env file based on .env_example (variable ENV change to "LOCAL"):
```
cat .env
```

### 5. Apply migrations
```
alembic upgrade head
```
> Don`t forget to change POSTGRES_HOST to "127.0.0.1" to run migrations from shell


## Run all containers:
With pre-installed make:
```
make start_all
```
Without pre-installed make:
```
docker-compose -f docker-compose.yaml up
```

## Run tests
```
poetry shell
pytest tests/
```

## Swagger:
http://localhost:8080/docs

## Docs:
http://localhost:8080/redoc
