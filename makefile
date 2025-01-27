DOCKER_COMPOSE = deployment/docker-compose.yml
SERVICE_NAME = auth

start:
	docker compose -f $(DOCKER_COMPOSE) up

stop:
	docker compose -f $(DOCKER_COMPOSE) down

build:
	docker compose -f $(DOCKER_COMPOSE) build

lint:
	docker compose -f $(DOCKER_COMPOSE) exec auth ruff check --fix 
	docker compose -f $(DOCKER_COMPOSE) exec admin ruff check --fix 

format:
	docker compose -f $(DOCKER_COMPOSE) exec auth poetry run black . 
	docker compose -f $(DOCKER_COMPOSE) exec admin poetry run black .

lint-fix: lint format


migrate:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) poetry run alembic upgrade head

poetry-update:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) poetry update

add:
	docker compose -f $(DOCKER_COMPOSE) exec $(service) poetry add $(package)


exp-requirements:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) poetry export --without-hashes -f requirements.txt -o requirements.txt 

autogenerate:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) alembic revision --autogenerate -m "revision"

migrate_db:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) python3 manage.py migrate


seed:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) python3 manage.py seed

.PHONY: start stop build lint migrate install exp-requirements poetry-update