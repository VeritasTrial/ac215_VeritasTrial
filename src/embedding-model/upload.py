"""The upload subcommand."""

import rich
from google.cloud import storage

from shared import (
    BUCKET_EMBEDDINGS_NPY_PATH,
    BUCKET_NAME,
    EMBEDDINGS_NPY_PATH,
    default_progress,
)


def main():
    if not EMBEDDINGS_NPY_PATH.exists():
        rich.print(
            f"[bold red]ERROR[/] Embeddings missing at: {EMBEDDINGS_NPY_PATH}; run the "
            "the embed subcommand first"
        )
        return

    # Connect to the GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(BUCKET_EMBEDDINGS_NPY_PATH)

    # Upload the embeddings to the bucket
    with default_progress() as progress:
        task = progress.add_task(f"Uploading data...", total=1)
        blob.upload_from_filename(EMBEDDINGS_NPY_PATH)
        progress.update(task, advance=1)

    rich.print(
        f"[bold green]->[/] Data uploaded to {BUCKET_EMBEDDINGS_NPY_PATH!r} in bucket "
        f"{BUCKET_NAME!r}"
    )
