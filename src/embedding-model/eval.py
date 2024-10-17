import chromadb
import numpy as np
import rich
from sklearn.metrics import roc_auc_score

from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
    get_model,
)

FETCH_CHROMADB_BATCH_SIZE = 1000
N_RANDOM_EMBEDDINGS = 30


def compute_matching_probabilities(query_emb, embs):
    """Compute probabilities of the query matching each given embedding."""
    # Compute cosine similarities
    query_emb_norm = np.linalg.norm(query_emb)
    similarities = [
        query_emb @ emb / (query_emb_norm * np.linalg.norm(emb)) for emb in embs
    ]

    # Apply softmax to convert similarities to probabilities
    e_similarities = np.exp(similarities - np.max(similarities))
    return e_similarities / e_similarities.sum()


def main(seed):
    rng = np.random.default_rng(seed)
    model = get_model()

    with default_progress() as progress:
        # Retrieve embeddings and documents from ChromaDB; we are doing so in batches so
        # that we can see a gradual progress
        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
        collection = client.get_collection(CHROMADB_COLLECTION_NAME)
        total_count = collection.count()
        task = progress.add_task(f"Retrieving embeddings...", total=total_count)
        all_ids, all_embeddings, all_documents = [], [], []
        for offset in range(0, total_count, FETCH_CHROMADB_BATCH_SIZE):
            results = collection.get(
                include=["embeddings", "documents"],
                limit=FETCH_CHROMADB_BATCH_SIZE,
                offset=offset,
            )
            all_ids.extend(results["ids"])
            all_embeddings.extend(results["embeddings"])
            all_documents.extend(results["documents"])
            progress.update(task, advance=len(results["ids"]))

        # Fetch embedding for each trial
        task = progress.add_task("Evaluating...", total=total_count)
        y_true, y_score, ranks = [], [], []
        for i, (target_embedding, target_title) in enumerate(
            zip(all_embeddings, all_documents)
        ):
            # Generate query embedding
            query_embedding = model.encode(f"Find the trial about {target_title}")

            # Get some random embeddings to compare against, where the last one is the
            # target embedding
            indices = np.delete(np.arange(total_count), i)
            indices = rng.choice(indices, N_RANDOM_EMBEDDINGS - 1, replace=False)
            random_embeddings = [all_embeddings[j] for j in indices]
            random_embeddings.append(target_embedding)

            # We would expect the target embedding to have the highest probabilitie of
            # matching the query
            true_labels = np.zeros(N_RANDOM_EMBEDDINGS)
            true_labels[-1] = 1
            y_true.extend(true_labels)

            # Compute actual probabilities of random embeddings matching the query
            scores = compute_matching_probabilities(query_embedding, random_embeddings)
            y_score.extend(scores)

            # Calculate rank of the target embedding, i.e., it is the rank-th most
            # likely to match the query
            rank = np.sum(scores > scores[-1]) + 1  # Ranks start from 1
            ranks.append(rank)

            progress.update(task, advance=1)

    # Calculate evaluation metrics
    auroc = roc_auc_score(y_true, y_score)
    mrr = sum(1.0 / rank for rank in ranks) / len(ranks)
    rich.print(f"[bold green]->[/] AUROC: {auroc:.3f} | MRR: {mrr:.3f}")
