import chromadb
from FlagEmbedding import FlagModel
import random
import numpy as np
import rich
from sklearn.metrics import roc_auc_score


from shared import (
    CHROMADB_COLLECTION_NAME,
    CHROMADB_HOST,
    CHROMADB_PORT,
    default_progress,
)

def get_random_embedding(all_ids, all_embeddings, exclude_index, n=30):
    # Create a list of indices excluding the target index
    indices = list(range(len(all_ids)))
    indices.pop(exclude_index)  # Remove the index of the target embedding

    # Randomly select n indices from the remaining indices
    random_indices = random.sample(indices, n)

    # Get the embeddings for the selected indices
    embeddings_list = [all_embeddings[i] for i in random_indices]

    return embeddings_list

def calculate_similarities_and_softmax(query_embedding, embeddings_list):
    def cosine_similarity(embedding1, embedding2):
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    def softmax(scores):
        e_scores = np.exp(scores - np.max(scores)) 
        return e_scores / e_scores.sum()

    scores = [cosine_similarity(query_embedding, emb) for emb in embeddings_list]

    # Apply softmax to convert scores to probabilities
    probabilities = softmax(scores)
    return probabilities    

def get_all_data(collection):
    total_count = collection.count()
    batch_size = 1000  # Adjust batch size as needed
    all_ids = []
    all_embeddings = []
    all_documents = []
    for offset in range(0, total_count, batch_size):
        results = collection.get(include=["embeddings", "documents"], limit=batch_size, offset=offset)
        all_ids.extend(results["ids"])
        all_embeddings.extend(results["embeddings"])
        all_documents.extend(results["documents"])
    return all_ids, all_embeddings, all_documents

def main():
    # Initialize true labels, predicted labels, and ranks
    true_labels = []
    predict_labels = []
    ranks = []

    # Connect to ChromaDB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(CHROMADB_COLLECTION_NAME)

    # Retrieve all embeddings, IDs, and documents from the collection
    print("Retrieving all data from ChromaDB...")
    all_ids, all_embeddings, all_documents = get_all_data(collection)
    total_count = len(all_ids)
    print(f"Total documents retrieved: {total_count}")

    # Define the embedding model
    model = FlagModel('BAAI/bge-small-en-v1.5', use_fp16=True)

    # Define number of random embeddings needed
    n = 30

    with default_progress() as progress:
        task = progress.add_task("Processing documents", total=total_count)

        # Fetch embedding for each trial
        for i in range(0, total_count):
            target_id = all_ids[i]
            target_embedding = all_embeddings[i]
            target_title = all_documents[i]

            # Generate query embedding
            query = f'Find the trial about {target_title}'
            query_embedding = model.encode(query)

            # Get random embeddings excluding the target embedding
            random_embeddings = get_random_embedding(all_ids, all_embeddings, i, n)
            random_embeddings.append(target_embedding)  # Append the target embedding

            scores = calculate_similarities_and_softmax(query_embedding, random_embeddings)

            predict_labels.extend(scores)
            true_labels.extend([0]*(len(scores)-1) + [1])

            # Calculate the rank of the target embedding
            sorted_scores = sorted(scores, reverse=True)
            target_score = scores[-1]
            rank = sorted_scores.index(target_score) + 1  # Ranks start at 1
            ranks.append(rank)

            # Update progress bar
            progress.update(task, advance=1)

    # Calculate evaluation metrics
    auroc = roc_auc_score(true_labels, predict_labels)
    mrr = sum(1.0 / rank for rank in ranks) / len(ranks)

    print(f'AUROC score is {auroc}, MRR is {mrr}')




