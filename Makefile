CORE_IMAGE_NAME=nnnxion/capy-world-core
BIBOON_IMAGE_NAME=nnnxion/capy-world-biboon
NGINX_IMAGE_NAME=nnnxion/capy-world-nginx
REDIS_IMAGE_NAME=nnnxion/capy-world-redis
TAG=latest

# development stuff
build:
	docker compose -f docker-compose.yaml build

run: build
	docker compose -f docker-compose.yaml up -d

down:
	docker compose -f docker-compose.yaml down

up:
	docker compose -f docker-compose.yaml down
	docker compose -f docker-compose.yaml up -d

# build service
build_core:
	docker build --target prod -t $(CORE_IMAGE_NAME):$(TAG) ./backend/core

build_biboon:
	docker build --target prod -t $(BIBOON_IMAGE_NAME):$(TAG) ./backend/biboon

build_nginx:
	docker build --target prod -t $(NGINX_IMAGE_NAME):$(TAG) ./nginx

build_redis:
	docker build -t $(REDIS_IMAGE_NAME):$(TAG) ./redis

# push service
push_core:
	docker push $(CORE_IMAGE_NAME):$(TAG)

push_biboon:
	docker push $(BIBOON_IMAGE_NAME):$(TAG)

push_nginx:
	docker push $(NGINX_IMAGE_NAME):$(TAG)

push_redis:
	docker push $(REDIS_IMAGE_NAME):$(TAG)

# releases
release_core: build_core push_core
release_biboon: build_biboon push_biboon
release_nginx: build_nginx push_nginx
release_redis: build_redis push_redis

release_all: release_core release_biboon release_nginx release_redis
