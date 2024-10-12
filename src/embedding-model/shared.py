"""Shared constants and utility functions."""

import os

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

CHROMADB_HOST = os.environ.get("CHROMADB_HOST", "localhost")
CHROMADB_PORT = os.environ.get("CHROMADB_PORT", 8000)
CHROMADB_COLLECTION_NAME = "veritas-trial-embeddings"


def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )
