"""The embed subcommand."""

import chromadb
import rich
from google.cloud import storage

import pandas as pd
import numpy as np
from io import StringIO
from FlagEmbedding import FlagModel


from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
    EMBED_NPY_PATH
)

BUCKET_NAME = "veritas-trial"
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"

def fetch_summary_from_bucket():
    # Connect to the GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    # Fetch data from the bucket and convert to DataFrame
    blob = bucket.get_blob(BUCKET_CLEANED_JSONL_PATH)
    jsonl_data_string = blob.download_as_bytes().decode('utf-8')
    jsonl_io = StringIO(jsonl_data_string)
    trials_df = pd.read_json(jsonl_io, lines=True)

    # Retrieve the summary column for embedding
    summaries = trials_df['summary'].to_list()
    # ids = trials_df['id'].to_list()
    # titles = trials_df['long_title']

    return summaries




def main():
    # Fetch data from bucket and extract the summaries
    summaries= fetch_summary_from_bucket()
    # Create embeddings with BGE-small-en-v1.5
    model = FlagModel('BAAI/bge-small-en-v1.5',use_fp16=True)
    embeddings = model.encode(summaries)

    # Save embeddings to a .npy file
    np.save(EMBED_NPY_PATH, embeddings)
    

    rich.print(
        "[bold green]->[/] Embeddings stored in collection "
        f"{CHROMADB_COLLECTION_NAME!r} in ChromaDB."
    )
