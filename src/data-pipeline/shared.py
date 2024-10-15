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
METADATA_PATH = DATA_DIR / "metadata.json"
RAW_JSONL_PATH = DATA_DIR / "raw_data.jsonl"
CLEANED_JSONL_PATH = DATA_DIR / "cleaned_data.jsonl"

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
