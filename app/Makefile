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

# [DEV] Run the backend server only; this should be run in a separate terminal
# window before running `devfrontend`
devbackend:
	docker-compose up chromadb backend --build

# [DEV] Run the frontend in development mode; this should be run in a separate
# terminal window when `devbackend` is running
devfrontend:
	cd frontend && VITE_BACKEND_URL=http://localhost:8001 pnpm dev

.PHONY: build run
