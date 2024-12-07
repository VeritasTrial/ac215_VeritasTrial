"""Shared constants and utility functions."""

import os
from io import StringIO
from pathlib import Path

import pandas as pd
import rich
from google.cloud import storage
from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

DATA_DIR = Path(__file__).parent / "data"
CLEANED_JSONL_PATH = DATA_DIR / "cleaned_data.jsonl"
EMBEDDINGS_NPY_PATH = DATA_DIR / "summary_embeddings.npy"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()

CHROMADB_HOST = os.getenv("CHROMADB_HOST", "localhost")
CHROMADB_PORT = os.getenv("CHROMADB_PORT", 8000)
CHROMADB_COLLECTION_NAME = "veritas-trial-embeddings"

BUCKET_NAME = "veritas-trial"
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"
BUCKET_EMBEDDINGS_NPY_PATH = f"embedding-model/bge_base_embedding.npy"


def default_progress():
    """Get a progress bar instance with default style."""
    return Progress(
        SpinnerColumn(),
        MofNCompleteColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    )


def get_cleaned_data():
    """Get the cleaned data from the bucket or reuse from local."""
    if CLEANED_JSONL_PATH.exists():
        # Reuse cleaned data if we have it locally
        with CLEANED_JSONL_PATH.open("r", encoding="utf-8") as f:
            studies_df = pd.read_json(f, lines=True)
    else:
        # Fetch cleaned data from the bucket and extract metadata
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        data_blob = bucket.get_blob(BUCKET_CLEANED_JSONL_PATH)
        data_io = StringIO(data_blob.download_as_text(encoding="utf-8"))
        studies_df = pd.read_json(data_io, lines=True)

        # Save the cleaned data locally for possible reuse
        with CLEANED_JSONL_PATH.open("w", encoding="utf-8") as f:
            data_io.seek(0)
            f.write(data_io.getvalue())

    return studies_df


def get_model():
    """Get the model used for embedding."""
    from FlagEmbedding import FlagModel

    model_name = "BAAI/bge-small-en-v1.5"
    rich.print(f"[bold green]->[/] Loading {model_name!r}...")
    return FlagModel(model_name, use_fp16=True)
