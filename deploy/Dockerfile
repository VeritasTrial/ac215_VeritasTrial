FROM ubuntu:22.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN set -ex; \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y build-essential curl software-properties-common apt-transport-https ca-certificates gnupg

# Install gcloud
# https://cloud.google.com/sdk/docs/install#deb
RUN set -ex; \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  apt-get update && \
  apt-get install -y google-cloud-cli

# Install Docker
# https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
RUN set -ex; \
  install -m 0755 -d /etc/apt/keyrings && \
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
  chmod a+r /etc/apt/keyrings/docker.asc && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list && \
  apt-get update && \
  apt-get install -y docker-ce

# Install Python
RUN set -ex; \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get update && \
  apt-get install -y python3.11 python3.11-distutils && \
  curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
  python3.11 get-pip.py

# Install Ansible
RUN set -ex; \
  python3.11 -m pip install requests ansible && \
  ansible-galaxy collection install community.docker

# Clean up
RUN set -ex; \
  rm -rf /var/lib/apt/lists/*

# Set up user and working directory; note that we are using root user for proper
# Docker-in-Docker permissions
RUN set -ex; \
  useradd -ms /bin/bash veritastrial -d /home/veritastrial -u 1000 -p "$(openssl passwd -1 Passw0rd)" && \
  usermod -aG docker veritastrial && \
  mkdir -p /veritastrial && \
  chown veritastrial:veritastrial /veritastrial
WORKDIR /veritastrial
COPY --chown=veritastrial:veritastrial . /veritastrial

# Run the entrypoint script on container startup
ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
