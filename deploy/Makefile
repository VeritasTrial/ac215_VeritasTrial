# Docker settings
DOCKER_CMD := docker
IMAGE_NAME := veritas-trial-deployment
CONTAINER_NAME := veritas-trial-deployment

all: build

# Build the Docker image
build:
	$(DOCKER_CMD) build -t $(IMAGE_NAME) .

# Run the Docker container and enter its interactive shell
run:
	$(DOCKER_CMD) container run -it --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/secrets/veritas-trial-deployment.json \
		--env GCP_PROJECT_ID=veritastrial \
		--env GCP_REGION=us-central1 \
		--volume $(PWD)/../secrets/veritas-trial-deployment.json:/secrets/veritas-trial-deployment.json:ro \
		--volume $(PWD)/../app/backend:/app/backend:ro \
		--volume $(PWD)/../app/frontend:/app/frontend:ro \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--name $(CONTAINER_NAME) $(IMAGE_NAME)

# Used by Github Actions; NOTE: the GOOGLE_APPLICATION_CREDENTIALS environment
# variable is set by the authentication action in the workflow and will be
# remapped inside the container
gh-actions:
	$(DOCKER_CMD) container run -it --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/secrets/veritas-trial-deployment.json \
		--env GCP_PROJECT_ID=veritastrial \
		--env GCP_REGION=us-central1 \
		--volume $(GOOGLE_APPLICATION_CREDENTIALS):/secrets/veritas-trial-deployment.json:ro \
		--volume $(PWD)/../app/backend:/app/backend:ro \
		--volume $(PWD)/../app/frontend:/app/frontend:ro \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) ./deploy-app.sh

.PHONY: build run
