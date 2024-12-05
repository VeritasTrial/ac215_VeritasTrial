# Docker settings
DOCKER_CMD := docker
IMAGE_NAME := veritas-trial-deployment
CONTAINER_NAME := veritas-trial-deployment

all: build

# Build the Docker image
build:
	$(DOCKER_CMD) build -t $(IMAGE_NAME) .

# Run the Docker container and enter its interactive shell, or run a command
run:
	$(DOCKER_CMD) container run $(if $(command),,-it) --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/secrets/veritas-trial-deployment.json \
		--env VERITAS_TRIAL_SERVICE_CREDENTIALS=/secrets/veritas-trial-service.json \
		--env GCP_PROJECT_ID=veritastrial \
		--env GCP_REGION=us-central1 \
		--env GCP_ZONE=us-central1-a \
		--volume $(PWD)/.docker-tag-app:/veritastrial/.docker-tag-app \
		--volume $(PWD)/../secrets/veritas-trial-deployment.json:/secrets/veritas-trial-deployment.json:ro \
		--volume $(PWD)/../secrets/veritas-trial-service.json:/secrets/veritas-trial-service.json:ro \
		--volume $(PWD)/../app/backend:/app/backend:ro \
		--volume $(PWD)/../app/frontend:/app/frontend:ro \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) $(command)

# Used by Github Actions
gh-actions:
	$(DOCKER_CMD) container run --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/secrets/veritas-trial-deployment.json \
		--env VERITAS_TRIAL_SERVICE_CREDENTIALS=/secrets/veritas-trial-service.json \
		--env GCP_PROJECT_ID=veritastrial \
		--env GCP_REGION=us-central1 \
		--env GCP_ZONE=us-central1-a \
		--volume $(PWD)/.docker-tag-app:/veritastrial/.docker-tag-app \
		--volume $(GOOGLE_APPLICATION_CREDENTIALS):/secrets/veritas-trial-deployment.json:ro \
		--volume $(VERITAS_TRIAL_SERVICE_CREDENTIALS):/secrets/veritas-trial-service.json:ro \
		--volume $(PWD)/../app/backend:/app/backend:ro \
		--volume $(PWD)/../app/frontend:/app/frontend:ro \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) $(command)

.PHONY: build run
