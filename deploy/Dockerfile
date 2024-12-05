FROM ubuntu:22.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN set -ex; \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y apt-transport-https build-essential ca-certificates curl gnupg jq software-properties-common

# Install gcloud
# https://cloud.google.com/sdk/docs/install#deb
RUN set -ex; \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  apt-get update && \
  apt-get install -y google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin

# Install Terraform
# https://developer.hashicorp.com/terraform/install?product_intent=terraform#linux
RUN set -ex; \
  curl -fsSL https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list && \
  apt-get update && \
  apt-get install -y terraform

# Install Kubernetes
# https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-using-native-package-management
RUN set -ex; \
  curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | \
    gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg && \
  chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg && \
  echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /" | \
    tee /etc/apt/sources.list.d/kubernetes.list && \
  chmod 644 /etc/apt/sources.list.d/kubernetes.list && \
  apt-get update && \
  apt-get install -y kubectl

# Install Helm
# https://helm.sh/docs/intro/install/#from-apt-debianubuntu
RUN set -ex; \
  curl https://baltocdn.com/helm/signing.asc | \
    gpg --dearmor | \
    tee /usr/share/keyrings/helm.gpg && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | \
    tee /etc/apt/sources.list.d/helm-stable-debian.list && \
  apt-get update && \
  apt-get install -y helm

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
  python3.11 -m pip install ansible google-auth kubernetes requests && \
  ansible-galaxy collection install community.docker google.cloud kubernetes.core

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
