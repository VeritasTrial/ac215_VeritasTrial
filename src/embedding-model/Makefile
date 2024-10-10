# Docker settings
DOCKER_CMD := docker
IMAGE_NAME := veritas-trial-embedding-model
CONTAINER_NAME := veritas-trial-embedding-model

all: build

# Build the Docker image
build:
	$(DOCKER_CMD) build -t $(IMAGE_NAME) .

# Run the Docker container and enter its interactive shell
run:
	$(DOCKER_CMD) container run -it --rm --name $(CONTAINER_NAME) $(IMAGE_NAME)

# [DEV] Update lock file and development environment on the host machine
devlock:
	pipenv lock
	pipenv sync -d

# [DEV] Format the codebase
devlint:
	black .
	ruff check --select I --fix .
	ruff format .

.PHONY: build run
