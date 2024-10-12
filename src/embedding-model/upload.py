"""The upload subcommand."""

import rich
from google.cloud import storage

from shared import CHROMADB_DIR

BUCKET_NAME = "veritas-trial"


def main():
    if not CHROMADB_DIR.exists():
        rich.print(
            f"[bold red]ERROR[/] ChromaDB missing: {CHROMADB_DIR}; run the embed "
            "subcommand first"
        )
        return

    # Connect to the GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    # TODO: use storage.transfer_manager.upload_many_from_filenames, see:
    # https://cloud.google.com/storage/docs/samples/storage-transfer-manager-upload-directory#code-sample
