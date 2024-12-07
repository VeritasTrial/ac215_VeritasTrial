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
            # This is a safeguard for None values, which are not allowed in
            # ChromaDB; we ensure not to leave numerical fields empty so we
            # safely replace with an empty string here
            stringfied[k] = ""
        elif isinstance(v, (list, dict)):
            stringfied[k] = json.dumps(v)
        else:
            stringfied[k] = v
    return stringfied


def main(host):
    # Check ChromaDB connection in the first place to avoid unnecessary work
    client = chromadb.HttpClient(host=host or CHROMADB_HOST, port=CHROMADB_PORT)

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

        # Insert embeddings and metadata to the vector database; we will first delete
        # the original collection if it exists to avoid conflicting data, then recreate
        # it with new data
        task = progress.add_task("Inserting data to ChromaDB...", total=1)
        for collection in client.list_collections():
            if collection.name == CHROMADB_COLLECTION_NAME:
                client.delete_collection(CHROMADB_COLLECTION_NAME)
                break
        collection = client.create_collection(CHROMADB_COLLECTION_NAME)
        collection.add(
            ids=study_ids,
            embeddings=embeddings.tolist(),
            documents=study_titles,
            metadatas=metadatas,
        )
        progress.update(task, advance=1)

    rich.print(
        f"[bold green]->[/] Data inserted to collection {CHROMADB_COLLECTION_NAME!r} "
        "in ChromaDB."
    )
