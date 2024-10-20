all: build run

build:
	docker-compose build

run:
	docker-compose up

# [DEV] Update lock files and development environment on the host machine
devlock:
	@cd backend && pipenv lock && pipenv sync -d && pipenv clean
	@cd frontend && pnpm install

# [DEV] Format the codebase
devlint:
	@cd backend && black . && ruff check --select I --fix . && ruff format .
	@cd frontend && pnpm format && pnpm lint

.PHONY: build run
