all: build run

build:
	docker-compose build

run:
	docker-compose up

# [DEV] Update lock files and development environment on the host machine
devlock:
	@cd backend && pipenv lock && pipenv sync -d && pipenv clean
	@cd frontend && pnpm install

# [DEV] Install development dependencies on the host machine based on the lock
# files without modifying them
devinstall:
	@cd backend && pipenv sync -d
	@cd frontend && pnpm install --frozen-lockfile

# [DEV] Format and lint the codebase
devlint:
	@cd backend && pipenv run bash -c "black . && ruff check --select I --fix . && ruff format . && mypy ."
	@cd frontend && pnpm format && pnpm lint

# [DEV] Check formatting and linting of the codebase
devlintcheck:
	@cd backend && pipenv run bash -c "black --check . && ruff check --select I . && mypy ."
	@cd frontend && pnpm format:check && pnpm lint:check

# [DEV] Run the backend server only; this should be run in a separate terminal
# window before running `devfrontend`
devbackend:
	docker-compose up chromadb backend --build

# [DEV] Run the frontend in development mode; this should be run in a separate
# terminal window when `devbackend` is running
devfrontend:
	cd frontend && VITE_BACKEND_URL=http://localhost:8001 pnpm dev

.PHONY: build run
