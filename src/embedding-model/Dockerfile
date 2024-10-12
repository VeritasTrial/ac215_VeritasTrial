FROM python:3.11-slim-buster

# Environment variabless
ENV DEBIAN_FRONTEND=noninteractive
ENV PYENV_SHELL=/bin/bash
ENV LANG=C.UTF-8
ENV PYTHONBUFFERED=1

# Install system dependencies and pipenv
RUN set -ex; \
  apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y build-essential curl && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir pipenv

# Set up user and working directory
RUN set -ex; \
  useradd -ms /bin/bash veritastrial -d /home/veritastrial -u 1000 -p "$(openssl passwd -1 Passw0rd)" && \
  mkdir -p /veritastrial && \
  chown veritastrial:veritastrial /veritastrial
USER veritastrial
WORKDIR /veritastrial

# Copy Pipfile and Pipfile.lock
COPY --chown=veritastrial:veritastrial Pipfile Pipfile.lock /veritastrial/

# Install Python dependencies and clear cache
RUN pipenv sync --clear && \
  rm -rf /home/veritastrial/.cache/pip && \
  rm -rf /home/veritastrial/.cache/pipenv

# Add the rest of the source code; this is done last to take advantage of
# Docker's layer caching mechanism
COPY --chown=veritastrial:veritastrial *.py Makefile /veritastrial/

# Activate the virtual environment on container startup
ENTRYPOINT [ "pipenv", "shell" ]
