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
CLEANED_JSONL_PATH = DATA_DIR / "cleaned_data.jsonl"
QA_JSON_PATH = DATA_DIR / "generated_qa.json"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

BUCKET_NAME = "veritas-trial"
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"

GENERATIVE_MODEL = "gemini-1.5-flash-001"


def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )
