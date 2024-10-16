"""Shared constants and utility functions."""

import os
from pathlib import Path

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

DATA_DIR = Path(__file__).parent / "data"
EMBEDDINGS_NPY_PATH = DATA_DIR / "summary_embeddings.npy"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

CHROMADB_HOST = os.environ.get("CHROMADB_HOST", "localhost")
CHROMADB_PORT = os.environ.get("CHROMADB_PORT", 8000)
CHROMADB_COLLECTION_NAME = "veritas-trial-embeddings"

BUCKET_NAME = "veritas-trial"
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"
BUCKET_EMBEDDINGS_NPY_PATH = f"embedding-model/{EMBEDDINGS_NPY_PATH.name}"


def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )
