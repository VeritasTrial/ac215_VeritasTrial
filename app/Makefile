all: build run

CHROMADB_HOST := $(shell cat $(PWD)/../deploy/chromadb/.instance-ip)

build:
	CHROMADB_HOST=$(CHROMADB_HOST) docker-compose build

run:
	CHROMADB_HOST=$(CHROMADB_HOST) docker-compose up

# [DEV] Update lock files and development environment on the host machine
devlockbackend:
	@cd backend && pipenv lock && pipenv sync -d && pipenv clean
devlockfrontend:
	@cd frontend && pnpm install
devlock:
	@$(MAKE) devlockbackend
	@$(MAKE) devlockfrontend

# [DEV] Install development dependencies on the host machine based on the lock
# files without modifying them
devinstallbackend:
	@cd backend && pipenv sync -d
devinstallfrontend:
	@cd frontend && pnpm install --frozen-lockfile
devinstall:
	@$(MAKE) devinstallbackend
	@$(MAKE) devinstallfrontend

# [DEV] Format and lint the codebase
devlintbackend:
	@cd backend && pipenv run bash -c "black . && ruff check --select I --fix . && ruff format . && mypy ."
devlintfrontend:
	@cd frontend && pnpm format && pnpm lint
devlint:
	@$(MAKE) devlintbackend
	@$(MAKE) devlintfrontend

# [DEV] Check formatting and linting of the codebase
devlintcheckbackend:
	@cd backend && pipenv run bash -c "black --check . && ruff check --select I . && mypy ."
devlintcheckfrontend:
	@cd frontend && pnpm format:check && pnpm lint:check
devlintcheck:
	@$(MAKE) devlintcheckbackend
	@$(MAKE) devlintcheckfrontend

# [DEV] Test the codebase; note we are only testing the backend
devtest:
	@cd backend && pipenv run pytest

# [DEV] Test the codebase and generate coverage reports; note we are only
# testing the backend
devtestcov:
	@cd backend && pipenv run bash -c "coverage run -m pytest && coverage report -m && coverage html"

# [DEV] Run the backend server only; this should be run in a separate terminal
# window before running `devfrontend`
devbackend:
	docker-compose up chromadb backend --build

# [DEV] Run the frontend in development mode; this should be run in a separate
# terminal window when `devbackend` is running
devfrontend:
	cd frontend && VITE_BACKEND_URL=http://localhost:8001 pnpm dev

.PHONY: build run
