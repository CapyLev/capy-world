build:
	docker compose -f docker-compose.yaml build

run: build
	docker compose -f docker-compose.yaml up -d

down:
	docker compose -f docker-compose.yaml down

up:
	docker compose -f docker-compose.yaml down
	docker compose -f docker-compose.yaml up -d
