rebuild:
	docker compose up --build capy-core-server --remove-orphans -d

makemigrations:
	docker exec -it capy_core_server ./manage.py makemigrations

migrate:
	docker exec -it capy_core_server ./manage.py migrate
