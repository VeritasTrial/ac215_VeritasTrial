"""The upload subcommand."""

import rich
from google.cloud import storage

from shared import EMBED_NPY_PATH, default_progress

BUCKET_NAME = "veritas-trial"


def main():
    if not EMBED_NPY_PATH.exists():
        rich.print(
            f"[bold red]ERROR[/] Cleaned data missing at: {EMBED_NPY_PATH}; run "
            "the clean subcommand first"
        )
        return

    # Connect to the GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    destination = f"embeddings/{EMBED_NPY_PATH.name}"
    blob = bucket.blob(destination)

    # Upload the cleaned data to the bucket
    with default_progress() as progress:
        task = progress.add_task(f"Uploading data...", total=1)
        blob.upload_from_filename(EMBED_NPY_PATH)
        progress.update(task, advance=1)

    rich.print(
        f"[bold green]->[/] Data uploaded to {destination!r} in bucket {BUCKET_NAME!r}"
    )