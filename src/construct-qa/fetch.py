"""The fetch subcommand."""

import rich
from google.cloud import storage

from shared import BUCKET_NAME, BUCKET_QA_JSON_PATH, QA_JSON_PATH, default_progress


def main():
    with default_progress() as progress:
        # Fetch the QA JSON file from the bucket; note that this will overwrite the
        # local file if it already exists
        task = progress.add_task("Fetching QA...", total=1)
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(BUCKET_QA_JSON_PATH)
        with QA_JSON_PATH.open("wb") as f:
            blob.download_to_file(f)
        progress.update(task, advance=1)

    rich.print(f"[bold green]->[/] QA fetched to: {QA_JSON_PATH}")
