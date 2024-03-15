DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml

.PHONY: up down

up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

dev-server:
	@poetry run poe serve

dev-client:
		@cd src/client && npm run dev

dev:
	@$(MAKE) dev-server & $(MAKE) dev-client
