DOCKER_COMPOSE = deployment/docker-compose.yml
SERVICE_NAME = auth
MULTIPLE_SERICES  =  admin auth

start:
	docker compose -f $(DOCKER_COMPOSE) up

stop:
	docker compose -f $(DOCKER_COMPOSE) down

build:
	docker compose -f $(DOCKER_COMPOSE) build

lint:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) ruff check --fix 

migrate:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) poetry run alembic upgrade head

poetry-update:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) poetry update


.PHONY: install
install:
	@if [ -z "$(package)" ]; then \
		echo "Error: package name not provided. Usage: make add-dep package=<package-name>"; \
		exit 1; \
	fi
	@for service in $(MULTIPLE_SERICES); do \
		echo "Adding $(package) to $$service service..."; \
		docker compose -f $(DOCKER_COMPOSE) exec $$service poetry add $(package); \
	done

add:
	docker compose -f $(DOCKER_COMPOSE) exec $(service) poetry add $(package)

.PHONY: remove
remove:
	@if [ -z "$(package)" ]; then \
		echo "Error: package name not provided. Usage: make remove-dep package=<package-name>"; \
		exit 1; \
	fi
	@for service in $(MULTIPLE_SERICES); do \
		echo "Removing $(package) from $$service service..."; \
		docker compose -f $(DOCKER_COMPOSE) exec $$service poetry remove $(package); \
	done

exp-requirements:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) poetry export --without-hashes -f requirements.txt -o requirements.txt 

autogenerate:
	docker compose -f $(DOCKER_COMPOSE) exec $(SERVICE_NAME) alembic revision --autogenerate -m "revision"

.PHONY: start stop build lint migrate install exp-requirements poetry-update