"""Shared constants and utility functions."""

from pathlib import Path
import os


from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

DATA_DIR = Path(__file__).parent / "data"
EMBED_NPY_PATH = DATA_DIR / "summary_embeddings.npy"

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
