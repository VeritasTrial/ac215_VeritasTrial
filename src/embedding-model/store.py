import io
from io import StringIO

import chromadb
import numpy as np
import pandas as pd
import rich
from google.cloud import storage

from shared import (
    BUCKET_CLEANED_JSONL_PATH,
    BUCKET_EMBEDDINGS_NPY_PATH,
    BUCKET_NAME,
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
)


def main():
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    with default_progress() as progress:
        task = progress.add_task("", total=4)

        # Fetch metadata from the cleaned data in the bucket
        progress.update(task, description="Fetching metadata...")
        data_blob = bucket.get_blob(BUCKET_CLEANED_JSONL_PATH)
        data_io = StringIO(data_blob.download_as_text(encoding="utf-8"))
        studies_df = pd.read_json(data_io, lines=True)
        study_ids = studies_df["id"].to_list()
        study_titles = studies_df["long_title"].to_list()
        progress.update(task, advance=1)

        # Fetch embeddings from the bucket
        progress.update(task, description="Fetching embeddings...")
        embeddings_blob = bucket.get_blob(BUCKET_EMBEDDINGS_NPY_PATH)
        embeddings_stream = io.BytesIO()
        embeddings_blob.download_to_file(embeddings_stream)
        embeddings_stream.seek(0)
        embeddings = np.load(embeddings_stream)
        progress.update(task, advance=1)

        # Connect to ChromaDB
        progress.update(task, description="Connecting to ChromaDB...")
        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
        collection = client.get_or_create_collection(CHROMADB_COLLECTION_NAME)
        progress.update(task, advance=1)

        # Upsert embeddings and the corresponding metadata to the vector database
        progress.update(task, description="Upserting data...")
        collection.upsert(
            ids=study_ids, embeddings=embeddings.tolist(), documents=study_titles
        )
        progress.update(task, advance=1)

    rich.print(
        f"[bold green]->[/] Data upserted to collection {CHROMADB_COLLECTION_NAME!r} "
        "in ChromaDB."
    )
