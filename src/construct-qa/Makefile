# Docker settings
DOCKER_CMD := docker
IMAGE_NAME := veritas-trial-construct-qa
CONTAINER_NAME := veritas-trial-construct-qa

all: build

# Build the Docker image
build:
	$(DOCKER_CMD) build -t $(IMAGE_NAME) .

# Run the Docker container and enter its interactive shell
run:
	$(DOCKER_CMD) container run -it --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/veritastrial/veritas-trial-service.json \
		--volume $(PWD)/../../secrets/veritas-trial-service.json:/veritastrial/veritas-trial-service.json:ro \
		--name $(CONTAINER_NAME) $(IMAGE_NAME)

# [DEV] Update lock file and development environment on the host machine
devlock:
	pipenv lock
	pipenv sync -d
	pipenv clean

# [DEV] Format the codebase
devlint:
	black .
	ruff check --select I --fix .
	ruff format .

.PHONY: build run
