#!/usr/bin/env python3.11
"""Model pipeline deployment script."""

import os
import uuid
from pathlib import Path

import google.cloud.aiplatform as aip
from kfp import compiler, dsl

BASE_DIR = Path(__file__).parent.parent
DOCKER_TAG_PATH = BASE_DIR / ".docker-tag-pipeline"

# GCP environment variables
GCP_REGION = os.getenv("GCP_REGION")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_PIPELINE_SERVICE_ACCOUNT_EMAIL = os.getenv("GCP_PIPELINE_SERVICE_ACCOUNT_EMAIL")

# Docker images
with DOCKER_TAG_PATH.open("r", encoding="utf-8") as f:
    DOCKER_TAG = f.read().strip()
REGISTRY_BASE = f"{GCP_REGION}-docker.pkg.dev/{GCP_PROJECT_ID}/docker"
DATA_PIPELINE_IMAGE = f"{REGISTRY_BASE}/veritas-trial-data-pipeline:{DOCKER_TAG}"
EMBEDDING_MODEL_IMAGE = f"{REGISTRY_BASE}/veritas-trial-embedding-model:{DOCKER_TAG}"

# Pipeline
PIPELINE_ROOT = f"gs://{GCP_PROJECT_ID}/pipeline-root"
PIPELINE_TEMPLATE = "pipeline.yaml"


@dsl.container_component
def data_pipeline():
    return dsl.ContainerSpec(image=DATA_PIPELINE_IMAGE, args=["./pipeline.sh"])


@dsl.container_component
def embedding_model():
    return dsl.ContainerSpec(image=EMBEDDING_MODEL_IMAGE, args=["./pipeline.sh"])


@dsl.pipeline
def pipeline():
    data_pipeline_task = data_pipeline().set_display_name("Data pipeline")
    embedding_model_task = (
        embedding_model()
        .set_display_name("Embedding model")
        .set_accelerator_type("NVIDIA_TESLA_T4")
        .set_accelerator_limit(1)
        .after(data_pipeline_task)
    )


def main():
    aip.init(project=GCP_PROJECT_ID, location=GCP_REGION)
    compiler.Compiler().compile(pipeline, PIPELINE_TEMPLATE)

    job = aip.PipelineJob(
        display_name=f"veritas-trial-deploy-pipeline-{uuid.uuid4()}",
        template_path=PIPELINE_TEMPLATE,
        pipeline_root=PIPELINE_ROOT,
    )
    job.run(service_account=GCP_PIPELINE_SERVICE_ACCOUNT_EMAIL)


if __name__ == "__main__":
    main()
