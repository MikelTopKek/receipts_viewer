# receipts_viewer
The test task is to develop a REST API for creating and viewing checks with user registration and authorization.

used Clean architecture with DDD elements

## Prerequisites

- Python 3.11
- pip
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


## Run all containers:
With pre-installed make:
```
make start_all
```
Without pre-installed make:
```
docker-compose -f docker-compose.yaml up
```


## Swagger:
http://localhost:8080/docs

## Docs:
http://localhost:8080/redoc
