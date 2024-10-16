"""The embed subcommand."""

from io import StringIO

import numpy as np
import pandas as pd
import rich
from FlagEmbedding import FlagModel
from google.cloud import storage

from shared import (
    BUCKET_CLEANED_JSONL_PATH,
    BUCKET_NAME,
    EMBEDDINGS_NPY_PATH,
    default_progress,
)


def main():
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    # Fetch cleaned data from the bucket
    with default_progress() as progress:
        task = progress.add_task("Fetching cleaned data...", total=1)
        blob = bucket.get_blob(BUCKET_CLEANED_JSONL_PATH)
        data_io = StringIO(blob.download_as_text(encoding="utf-8"))
        studies_df = pd.read_json(data_io, lines=True)
        progress.update(task, advance=1)

    # Load the model and encode the summaries, then save the embeddings as binary
    # TODO: strangely use_fp16=True in the container still gives float32 embeddings
    rich.print("[bold green]->[/] Creating vector embeddings...")
    model = FlagModel("BAAI/bge-small-en-v1.5", use_fp16=True)
    embeddings = model.encode(studies_df["summary"].to_list())
    np.save(EMBEDDINGS_NPY_PATH, embeddings)

    rich.print(f"[bold green]->[/] Embeddings saved to {EMBEDDINGS_NPY_PATH}")
