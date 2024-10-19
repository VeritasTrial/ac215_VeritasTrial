"""Shared constants and utility functions."""

from pathlib import Path

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

# Project configuration used for Vertex AI
GCP_PROJECT_ID = "veritastrial"
GCP_PROJECT_LOCATION = "us-central1"

DATA_DIR = Path(__file__).parent / "data"
TEMP_TRAIN_JSONL_PATH = DATA_DIR / "temp_train.jsonl"
TEMP_TEST_JSONL_PATH = DATA_DIR / "temp_test.jsonl"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

BUCKET_NAME = "veritas-trial"
BUCKET_FINETUNE_DATA_DIR = "finetune-data"

# Mapping of dataset names to their remote paths in GCS
DATASET_MAPPING = {
    "qa": "construct-qa/instruction.jsonl",
    "pubmed-qa": "external/pubmed-qa.jsonl",
}


def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )
