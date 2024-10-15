import chromadb
import rich
from google.cloud import storage

import pandas as pd
import numpy as np
import io
from io import StringIO

from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
    EMBED_NPY_PATH
)

BUCKET_NAME = 'veritas-trial'
BUCKET_CLEANED_JSONL_PATH = "data-pipeline/cleaned_data.jsonl"
BUCKET_EMB_NPY_PATH = 'embeddings/trial_embedding.npy'


def fetch_data_from_bucket():
    # Connect to the GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    # Fetch data from the bucket and convert to DataFrame
    blob_json = bucket.get_blob(BUCKET_CLEANED_JSONL_PATH)
    jsonl_data_string = blob_json.download_as_bytes().decode('utf-8')
    jsonl_io = StringIO(jsonl_data_string)
    trials_df = pd.read_json(jsonl_io, lines=True)

    # Fetch the embedding from GCP Bucket
    blob_emb = bucket.get_blob(BUCKET_EMB_NPY_PATH)
    if blob_emb:
        byte_stream = io.BytesIO()
        blob_emb.download_to_file(byte_stream)
        byte_stream.seek(0) 
        embeddings = np.load(byte_stream)
    else:
        print("No blob found for the given path.")

    # Retrieve the meta data column for embedding
    ids = trials_df['id'].to_list()
    titles = trials_df['long_title'].to_list()

    return ids, titles, embeddings


def query_data():
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(CHROMADB_COLLECTION_NAME)
    
    # Example of querying by ID (adjust according to your API/client capabilities)
    sample_id = 'NCT02371889'
    document = collection.get(ids=[sample_id],include=['embeddings', 'documents', 'metadatas'])
    print("Retrieved Document:", document)



def main():
    try:
        ids, titles, embeddings = fetch_data_from_bucket()

        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
        collection = client.get_or_create_collection(CHROMADB_COLLECTION_NAME)
        
        # Upsert embeddings to the database
        collection.upsert(
            ids=ids,
            embeddings=embeddings.tolist(),  
            documents=titles
        )
        print("Data upserted successfully.")
        query_data()
    except Exception as e:
        print(f"An error occurred: {e}")
