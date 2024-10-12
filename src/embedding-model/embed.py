"""The embed subcommand."""

import chromadb
import rich
from google.cloud import storage

from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
)

BUCKET_NAME = "veritas-trial"
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"


def main():
    # Connect to the GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    # TODO: fetch data from the bucket

    # TODO: create embeddings with BGE-M3

    # Store embeddings in the ChromaDB vector database
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_or_create_collection(CHROMADB_COLLECTION_NAME)
    # TODO: upsert embeddings to the database
    # collection.upsert(
    #     ids=["id1"],
    #     embeddings=[[1, 2, 3]],
    #     metadatas=[{}],
    #     documents=["Document 1"],
    # )

    rich.print(
        "[bold green]->[/] Embeddings stored in collection "
        f"{CHROMADB_COLLECTION_NAME!r} in ChromaDB."
    )
