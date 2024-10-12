# Docker settings
DOCKER_CMD := docker
IMAGE_NAME := veritas-trial-embedding-model
CONTAINER_NAME := veritas-trial-embedding-model
CONTAINER_NAME_CHROMADB := veritas-trial-chromadb
NETWORK_NAME := veritas-trial-network

all: build

# Build the Docker image
build:
	$(DOCKER_CMD) build -t $(IMAGE_NAME) .

# Create a Docker network if it does not exist
network:
	@NETWORK_ID=$$(docker network ls -q -f "name=^$(NETWORK_NAME)$$"); \
		if [ -z "$$NETWORK_ID" ]; then \
			echo "Creating network: $(NETWORK_NAME)"; \
			$(DOCKER_CMD) network create $(NETWORK_NAME); \
		else \
			echo "Network already exists: $$NETWORK_ID"; \
		fi

# Run ChromaDB server in the background if it is not running
chromadb: network
	@CONTAINER_ID_CHROMADB=$$(docker ps -q -f "name=^$(CONTAINER_NAME_CHROMADB)$$"); \
		if [ -z "$$CONTAINER_ID_CHROMADB" ]; then \
			echo "Creating ChromaDB server: $(CONTAINER_NAME_CHROMADB)"; \
			$(DOCKER_CMD) container run -d --rm \
				--publish 8000:8000 \
				--network $(NETWORK_NAME) \
				--volume chroma-data:/chroma/chroma \
				--name $(CONTAINER_NAME_CHROMADB) chromadb/chroma; \
		else \
			echo "ChromaDB server already running: $$CONTAINER_ID_CHROMADB"; \
		fi

# Run the Docker container and enter its interactive shell
run: chromadb
	$(DOCKER_CMD) container run -it --rm \
		--env CHROMADB_HOST=$(CONTAINER_NAME_CHROMADB) \
		--network $(NETWORK_NAME) \
		--name $(CONTAINER_NAME) $(IMAGE_NAME)

# Get information of the running networks and containers
info:
	@echo "Network  : $$(docker network ls -q -f "name=^$(NETWORK_NAME)$$")"
	@echo "ChromaDB : $$(docker ps -q -f "name=^$(CONTAINER_NAME_CHROMADB)$$")	"

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
