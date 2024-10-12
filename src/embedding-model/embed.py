"""The embed subcommand."""

import chromadb
import rich

from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
)


def main():
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_or_create_collection(CHROMADB_COLLECTION_NAME)

    # TODO: fetch data from GCS

    # TODO: create embeddings with BGE-M3

    # TODO: upsert embeddings to ChromaDB
    # collection.upsert(
    #     ids=["id1"],
    #     embeddings=[[1, 2, 3]],
    #     metadatas=[{}],
    #     documents=["Document 1"],
    # )

    rich.print(
        f"[bold green]->[/] Embeddings stored in collection {CHROMADB_COLLECTION_NAME} "
        "in ChromaDB."
    )
