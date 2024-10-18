"""Shared constants and utility functions."""

from pathlib import Path

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

DATA_DIR = Path(__file__).parent / "data"
GCP_PROJECT = "veritastrial"
GCP_LOCATION = "us-central1"
GENERATIVE_MODEL = "gemini-1.5-flash-001"
OUTPUT_FOLDER = "data" 
BUCKET_NAME = "veritas-trial"
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )
