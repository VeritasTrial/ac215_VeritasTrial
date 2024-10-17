import chromadb
import rich

from shared import CHROMADB_COLLECTION_NAME, CHROMADB_HOST, CHROMADB_PORT, get_model


def main(query, top_k):
    """Evaluate the query against the database and return top_k results."""
    model = get_model()

    # Generate embedding vector for the query text
    rich.print("[bold green]->[/] Creating query embedding...")
    query_embedding = model.encode(query)

    # Query the ChromaDB vector database
    rich.print(f"[bold green]->[/] Searching for top {top_k} matches...")
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(CHROMADB_COLLECTION_NAME)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances", "metadatas"],
    )

    # Print the results; note that we are taking the first entry in each result field
    # because we are querying wiht a single embedding vector
    n_digits = len(str(top_k))
    for i, (nctid, doc, dist) in enumerate(
        zip(results["ids"][0], results["documents"][0], results["distances"][0]),
        start=1,
    ):
        rich.get_console().print(
            f"[green][{i:0{n_digits}d}][/] {doc} [dim]{nctid} ({dist=:.3f})[/]",
            highlight=False,
        )
