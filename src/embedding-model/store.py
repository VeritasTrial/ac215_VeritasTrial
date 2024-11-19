import json
from io import BytesIO

import chromadb
import numpy as np
import rich
from google.cloud import storage

from shared import (
    BUCKET_EMBEDDINGS_NPY_PATH,
    BUCKET_NAME,
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    EMBEDDINGS_NPY_PATH,
    default_progress,
    get_cleaned_data,
)


def stringify_metadata(metadata):
    """Stringify metadata so each value is either string or numeric."""
    stringfied = {}
    for k, v in metadata.items():
        if v is None:
            # Numeric None values are automatically converted to NaN in the
            # dataframe so we can safely convert the rest to empty strings
            stringfied[k] = ""
        elif isinstance(v, (list, dict)):
            stringfied[k] = json.dumps(v)
        else:
            stringfied[k] = v
    return stringfied


def main():
    with default_progress() as progress:
        # Get metadata that will be paired with the embeddings to be stored in the
        # vector database
        task = progress.add_task("Fetching cleaned data...", total=1)
        studies_df = get_cleaned_data()
        study_ids = studies_df["id"].to_list()
        study_titles = studies_df["short_title"].to_list()
        metadatas = studies_df.apply(
            lambda row: stringify_metadata(row), axis=1
        ).tolist()
        del studies_df
        progress.update(task, advance=1)

        # Fetch embeddings from the bucket or reuse from local
        task = progress.add_task("Fetching embeddings...", total=1)
        if EMBEDDINGS_NPY_PATH.exists():
            embeddings = np.load(EMBEDDINGS_NPY_PATH)
        else:
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            embeddings_blob = bucket.get_blob(BUCKET_EMBEDDINGS_NPY_PATH)
            embeddings_stream = BytesIO()
            embeddings_blob.download_to_file(embeddings_stream)
            embeddings_stream.seek(0)
            embeddings = np.load(embeddings_stream)
            # Save the embeddings locally for possible reuse; the embed subcommand
            # always overwrites so this is safe
            np.save(EMBEDDINGS_NPY_PATH, embeddings)
        progress.update(task, advance=1)

        # Upsert embeddings and the corresponding metadata to the vector database
        task = progress.add_task("Upserting data to ChromaDB...", total=1)
        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
        collection = client.get_or_create_collection(CHROMADB_COLLECTION_NAME)
        collection.upsert(
            ids=study_ids,
            embeddings=embeddings.tolist(),
            documents=study_titles,
            metadatas=metadatas,
        )
        progress.update(task, advance=1)

    rich.print(
        f"[bold green]->[/] Data upserted to collection {CHROMADB_COLLECTION_NAME!r} "
        "in ChromaDB."
    )
