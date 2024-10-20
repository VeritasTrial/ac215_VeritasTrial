# AC215 | Milestone 2 | VeritasTrial

- **Team Members:** Yao Xiao, Bowen Xu, Tong Xiao.
- **Group Name:** VeritasTrial

## Background

The rapid growth of clinical trial data, particularly from large repositories like ClinicalTrials.gov, presents significant opportunities for improving healthcare research and patient outcomes. However, the sheer volume of data makes it challenging for researchers, clinicians, and patients to easily find and understand specific trials relevant to their needs. 

To address this, we aim to develop an AI-powered application that enhances the information retrieval process for clinical trials. Leveraging state-of-the-art embedding models, the system will retrieve relevant trials from ClinicalTrials.gov based on user queries. Following retrieval, a conversational AI chatbot will enable users to discuss specific details about a trial, including endpoints, results, and eligibility criteria, providing an intuitive and interactive experience. This innovative approach seeks to streamline access to critical information, fostering more informed decisions in clinical research and patient care.

## Objective

This project aims to develop an AI-powered system that enables users to efficiently search and explore clinical trials within a database. The system will utilize a fine-tuned language model (LLM) to identify and retrieve the most relevant trials based on user queries. It will then allow users to interact with specific trials and provide accurate responses by leveraging both the fine-tuned model and structured clinical trial data stored in the database.

## Pipeline

![49d3be580e15094a994c21cbd1c16fb](https://github.com/user-attachments/assets/78dcfd73-b9bc-43e6-8c3b-d281fb499694)

In particular, we have four separate containers for our pipeline. Please see their respective directories for details:

- [data-pipeline](./src/data-pipeline/): Collect and clean datasets.
- [embedding-model](./src/embedding-model/): Create vector database for querying.
- [construct-qa](./src/construct-qa/): Construct QA pairs for finetuning.
- [finetune-model](./src/finetune-model/): Finetune the model.

As follows is a screenshot of all our four containers running:

![image](https://github.com/user-attachments/assets/6dd8f8e7-fe0f-4fd0-9f06-70ddb0f088c8)

## Data Collection

We collected clinical trial data from [ClinicalTrials.gov](https://clinicaltrials.gov/) and filtered 22K data with results. These are used both for creating our vector database, and for finetuning after construted into QA pairs. We also collected 211K medical QA data from the [PubMedQA](https://huggingface.co/datasets/qiaojin/PubMedQA) dataset and used a subset for finetuning, mixed with our constructed QA.

## Embedding Model

We used a small version of the [BGE](https://huggingface.co/BAAI/bge-small-en-v1.5) model for constructing our vector database (using ChromaDB). We have validated the quality of our embeddings by generating N random samples, with one of them being the correct sample, and see if the model can accurately retrieve the correct one. Both the AUROC score (area under the receiver operating characteristic curve) and the MRR score (mean reciprocal rank) are above 0.99, meaning high retrieval accuracy.

## Finetuning Results

We finetuned the Gemini 1.5 Flash model (gemini-1.5-flash-002) with 29,800 messages (15,764,259 tokens) and 3 epochs. The learing rate muliplier is 0.1 and the adapter size is 4. No sample is too long to be truncated. The training metrics during the supervised finetuning progress are as follows:

<img width="300" alt="Total loss" src="https://github.com/user-attachments/assets/8ba85aaa-2f71-4f84-bbc5-7758b57edeed">
<img width="300" alt="Num predictions" src="https://github.com/user-attachments/assets/bc84b82b-b296-4fe2-8396-7690c7a1fa67">
<img width="300" alt="Fraction of correct next step preds" src="https://github.com/user-attachments/assets/e5491f66-e0a5-442b-be90-b25c006c797c">

The validation metrics (on a validation set of size 256) during the supervised finetuning progress are as follows:

<p align="center">
  <img width="300" alt="Total loss (validation)" src="https://github.com/user-attachments/assets/9c85ed42-22f0-4066-809d-16cda275fa2d">
  <img width="300" alt="Num predictions (validation)" src="https://github.com/user-attachments/assets/9595733a-19c6-4ea9-b4ee-bca1bcb38922">
  <img width="300" alt="Fraction of correct next step preds (validation)" src="https://github.com/user-attachments/assets/7d1c4a04-3f8e-4d13-a9fc-781375758068">
</p>

## App Preliminary Designs

Here is a preliminary design of how our app may be composed:

<details>
<summary>docker-compose.yaml</summary>
<p>

```yaml
services:
  # ChromaDB - Query the vector database
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma-data:/chroma/chroma
  # Backend service - This will serve the embedding model and the finetuned LLM;
  # for the embedding model it can load BGE to embed user query then query the
  # vector database for relevant results; for the finetuned LLM it will utilize
  # the Vertex AI endpoint
  backend:
    build:
      context: ./backend
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/secrets/veritas-trial-service.json
    ports:
      - "8001:8001"
    volumes:
      - ../secrets:/secrets
    depends_on:
      - chromadb
  # Frontend service - This will be the frontend interface built with React; it
  # will query the service exposed by the backend; the frontend can be accessed
  # at http://localhost:8080
  frontend:
    build:
      context: ./frontend
      args:
        VITE_BACKEND_URL: http://backend:8001
    ports:
      - "8080:80"
    depends_on:
      - backend

volumes:
  # We will reuse the ChromaDB volume created when creating the vector database
  chroma-data:
    external: true
```

</p>
</details>

<details>
<summary>backend/Dockerfile</summary>
<p>

```Dockerfile
FROM python:3.11-slim-bookworm

# Environment variables
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
  rm -rf /home/veritastrial/.cache/pip/* && \
  rm -rf /home/veritastrial/.cache/pipenv/*

# Add the rest of the source code; this is done last to take advantage of
# Docker's layer caching mechanism
COPY --chown=veritastrial:veritastrial *.py /veritastrial/

# Run the app on port 8001
EXPOSE 8001
CMD [ "pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001" ]
```

</p>
</details>

<details>
<summary>frontend/Dockerfile</summary>
<p>

```Dockerfile
FROM node:20-bookworm-slim as build

# Environment variables
ENV PNPM_HOME=/pnpm
ENV PATH=${PNPM_HOME}:${PATH}
RUN corepack enable

# Copy package.json and pnpm-lock.yaml
WORKDIR /app
COPY package.json pnpm-lock.yaml ./

# Install node modules
RUN pnpm install --frozen-lockfile

# Environment variables for the vite build
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}

# Add the rest of the source code and build the app; this is done last to take
# advantage of Docker's layer caching mechanism
COPY . ./
RUN pnpm build

# Nginx wrapper to serve static files
FROM nginx:stable
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;" ]
```

</p>
</details>

Here is an example of what the app interface may look like:

<img width="300" alt="6c82ae3fc63718a00f5b225fc49e447" src="https://github.com/user-attachments/assets/3ac90b63-92d0-48d9-a791-39ee5ae98938">
<img width="300" alt="0251530ead34fc048822cfb2feacc95" src="https://github.com/user-attachments/assets/d2c419c9-c04e-404f-ab1b-55763c713b08">
<img width="300" alt="4170d338f651db1b31cabccadb8ea88" src="https://github.com/user-attachments/assets/ec3e74fa-f6ae-47db-8d10-74922caf9213">
