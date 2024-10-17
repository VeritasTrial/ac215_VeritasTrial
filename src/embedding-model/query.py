import chromadb
from FlagEmbedding import FlagModel

from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
)

def retrieve_top_k(query_text, k=10):
    """Retrieve the top K results based on the query text."""
    # Generate query embedding
    model = FlagModel('BAAI/bge-small-en-v1.5', use_fp16=True)
    query_embedding = model.encode(query_text)

    # Connect to ChromaDB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(CHROMADB_COLLECTION_NAME)

    # Perform the search
    results = collection.query(query_embeddings=[query_embedding], n_results=k, include=['documents'])
    return results

def main(query_text, top_k=10):
    """Evaluate the query against the database and return top_k results."""
    # Call the retrieve function
    results = retrieve_top_k(query_text, top_k)

    # Print or process the results as needed
    print(f"Top {top_k} results for query '{query_text}':")
    for i, result in enumerate(results['documents'], start=1):
        print(f"{i}. {result}")
