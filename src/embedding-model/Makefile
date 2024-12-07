# Docker settings
DOCKER_CMD := docker
IMAGE_NAME := veritas-trial-embedding-model
CONTAINER_NAME := veritas-trial-embedding-model
CHROMADB_HOST := $(shell cat $(PWD)/../../deploy/chromadb/.instance-ip)

all: build

# Build the Docker image
build:
	$(DOCKER_CMD) build -t $(IMAGE_NAME) .

# Run the Docker container and enter its interactive shell or run a command
run:
	$(DOCKER_CMD) container run $(if $(command),,-it) --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/secrets/veritas-trial-deployment.json \
		--env CHROMADB_HOST=$(CHROMADB_HOST) \
		--env CHROMADB_PORT=8000 \
		--volume $(PWD)/../../secrets/veritas-trial-deployment.json:/secrets/veritas-trial-deployment.json:ro \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) $(command)

# [DEV] Update lock file and development environment on the host machine
devlock:
	pipenv lock
	pipenv sync -d
	pipenv clean

# [DEV] Format the codebase
devlint:
	pipenv run bash -c "black . && ruff check --select I --fix . && ruff format . && mypy ."

.PHONY: build run
