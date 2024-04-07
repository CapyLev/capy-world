build:
	docker compose -f docker-compose.yaml build

run: build
	docker compose -f docker-compose.yaml up

up:
	docker compose -f docker-compose.yaml up

down:
	docker compose -f docker-compose.yaml down

rerun:
	docker compose -f docker-compose.yaml down
	docker compose -f docker-compose.yaml up
