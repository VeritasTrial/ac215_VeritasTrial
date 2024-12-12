# Docker settings
DOCKER_CMD := docker
IMAGE_NAME := veritas-trial-construct-qa
CONTAINER_NAME := veritas-trial-construct-qa

all: build

# Build the Docker image
build:
	$(DOCKER_CMD) build -t $(IMAGE_NAME) .

# Run the Docker container and enter its interactive shell or run a command
run:
	$(DOCKER_CMD) container run $(if $(command),,-it) --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/secrets/veritas-trial-deployment.json \
		--volume $(PWD)/../../secrets/veritas-trial-deployment.json:/secrets/veritas-trial-deployment.json:ro \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) $(command)

# [DEV] Update lock file and development environment on the host machine
devlock:
	pipenv lock
	pipenv sync -d
	pipenv clean

# [DEV] Install development dependencies on the host machine based on the lock
# file without modifying it
devinstall:
	pipenv sync -d
	pipenv clean

# [DEV] Format the codebase
devlint:
	pipenv run bash -c "black . && ruff check --select I --fix . && ruff format . && mypy ."

.PHONY: build run
