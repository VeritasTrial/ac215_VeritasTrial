"""Shared constants and utility functions."""

from pathlib import Path

import jsonlines
from google.cloud import storage
from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

DATA_DIR = Path(__file__).parent / "data"
ERRORS_DIR = DATA_DIR / "errors"
CLEANED_JSONL_PATH = DATA_DIR / "cleaned_data.jsonl"
QA_JSON_PATH = DATA_DIR / "generated_qa.json"
INSTRUCTION_JSONL_PATH = DATA_DIR / "instruction.jsonl"

BUCKET_NAME = "veritas-trial"
BUCKET_QA_JSON_PATH = "construct-qa/generated_qa.json"
BUCKET_INSTRUCTION_JSONL_PATH = "construct-qa/instruction.jsonl"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

if not ERRORS_DIR.exists():
    ERRORS_DIR.mkdir()

BUCKET_NAME = "veritas-trial"
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"

GENERATIVE_MODEL = "gemini-1.5-flash-001"


def get_cleaned_data():
    """Get the cleaned data from the bucket or reuse from local."""
    if not CLEANED_JSONL_PATH.exists():
        # Fetch cleaned data from the bucket and store locally if is not already
        # locally available
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        data_blob = bucket.get_blob(BUCKET_CLEANED_JSONL_PATH)
        with CLEANED_JSONL_PATH.open("wb") as f:
            data_blob.download_to_file(f)

    with jsonlines.open(CLEANED_JSONL_PATH, "r") as f:
        studies = [study for study in f]
    return studies


def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )
