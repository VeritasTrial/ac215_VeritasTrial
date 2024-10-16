import sys
import chromadb
from FlagEmbedding import FlagModel


from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
)


def retrieve_top_k(query_text, k=10):
    #Generate query embedding
    model = FlagModel('BAAI/bge-small-en-v1.5', use_fp16= True)
    query_embedding = model.encode(query_text)

    # Connect to ChromaDB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(CHROMADB_COLLECTION_NAME)
    
    # Perform the search
    results = collection.query(query_embedding, n_results=k, include=[])
    return results


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py 'query_text'")
        sys.exit(1)

    query_text = sys.argv[1]
    results = retrieve_top_k(query_text)
    print(results)
