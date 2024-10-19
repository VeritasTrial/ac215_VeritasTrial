"""The upload subcommand."""

import rich
from google.cloud import storage

from shared import (
    BUCKET_INSTRUCTION_JSONL_PATH,
    BUCKET_NAME,
    BUCKET_QA_JSON_PATH,
    INSTRUCTION_JSONL_PATH,
    QA_JSON_PATH,
    default_progress,
)

PATH_MAPPING = [
    (QA_JSON_PATH, BUCKET_QA_JSON_PATH),
    (INSTRUCTION_JSONL_PATH, BUCKET_INSTRUCTION_JSONL_PATH),
]


def main():
    for local_path, _ in PATH_MAPPING:
        if not local_path.exists():
            rich.print(
                f"[bold red]Error:[/] Data missing at: {local_path}; run the generate "
                "and prepare subcommands first"
            )
            return

    # Initialize GCP storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    # Upload the QA dataset and constructed instruction datasets
    with default_progress() as progress:
        task = progress.add_task("Uploading files...", total=len(PATH_MAPPING))
        for local_path, remote_path in PATH_MAPPING:
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_path)
            progress.update(task, advance=1)

    for _, remote_path in PATH_MAPPING:
        rich.print(
            f"[bold green]->[/] Data uploaded to {remote_path!r} in bucket "
            f"{BUCKET_NAME!r}"
        )
