build:
	docker compose -f docker-compose.yaml build

run: build
	docker compose -f docker-compose.yaml up -d

down:
	docker compose -f docker-compose.yaml down

up:
	docker compose -f docker-compose.yaml down
	docker compose -f docker-compose.yaml up -d

build_core:
	docker build --target dev -t capy-core-server ./backend/core

build_biboon:
	docker build --target dev -t capy-biboon-server ./backend/biboon
