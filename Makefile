.PHONY: help
help: ## Show this help (usage: make help)
	@echo "Usage: make [target]"
	@echo "Targets:"
	@awk '/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			target = $$1; \
			sub(/:/, "", target); \
			printf "  \033[36m%-20s\033[0m %s\n", target, substr($$0, RSTART + 3, RLENGTH); \
		} \
	}' $(MAKEFILE_LIST)


.PHONY: build
build:
	docker compose up --build

.PHONY: up
up:	#
	docker compose up

.PHONY: down
down:
	docker compose down --remove-orphans | true


.PHONY: autogenerate
autogenerate:
	docker compose up -d | true
	docker compose exec app alembic revision --autogenerate -m "$(msg)"

.PHONY: downgrade
downgrade:
	docker compose up -d | true
	docker compose exec app alembic downgrade -1

.PHONY: downgrade_to
downgrade_to:
	docker compose up -d | true
	docker compose exec app alembic downgrade "$(revision)"
