start_all:
	docker compose -f docker-compose.yaml up
	
start_db:
	docker compose -f docker-compose.yaml up db

start_backend:
	docker compose -f docker-compose.yaml up backend --build
	