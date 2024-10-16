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


def get_random_embedding(collection, exclude_id, n = 30):
    total_count = collection.count()
    embeddings_list = []
    # Get n random embeddings from collection
    for i in range(n):
        random_offset = random.randint(0, total_count-1)
        result = collection.get(include=['embeddings'], 
                                limit=1, offset=random_offset)
        if result['ids'][0] != exclude_id:
            embeddings_list.append(result['embeddings'][0])

    return embeddings_list

def calculate_similarities_and_softmax(query_embedding, random_embeddings):

    def cosine_similarity(embedding1, embedding2):
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    def softmax(scores):
        e_scores = np.exp(scores - np.max(scores)) 
        return e_scores / e_scores.sum()

    scores = [cosine_similarity(query_embedding, emb) for emb in random_embeddings]

    # Apply softmax to convert scores to probabilities
    probabilities = softmax(scores)
    return probabilities    


def main():
    # Initialize true labels, precidt labels and ranks
    true_labels = []
    predict_labels = []
    ranks = []

    # Connect to ChromaDB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(CHROMADB_COLLECTION_NAME)

    # Define the embedding model
    model = FlagModel('BAAI/bge-small-en-v1.5', use_fp16= True)

    # Define # of random embeddings needed
    n = 30
    total_count = collection.count()

    with default_progress() as progress:
        task = progress.add_task("Processing documents", total=total_count)
        for i in range(0, total_count):
            target = collection.get(
                include=["documents", "embeddings"],
                limit=1,
                offset=i)
            target_id = target['ids'][0]
            target_embedding = target['embeddings'][0]
            target_title = target['documents'][0]

            # generate query_embedding
            query = f'Find the trial about {target_title}'
            query_embedding = model.encode(query)
            random_embeddings = get_random_embedding(collection, target_id)
            random_embeddings.append(target_embedding)

            scores = calculate_similarities_and_softmax(query_embedding, random_embeddings)
            predict_labels.extend(scores)
            true_labels.extend([0]*n + [1])

            rank = sum(1 for x in scores if x <= scores[-1])
            ranks.append(rank)

            # Update progress bar
            progress.update(task, advance=1)

    auroc = roc_auc_score(true_labels, predict_labels)
    mrr = sum(1.0 / rank for rank in ranks) / len(ranks)

    print(f'AUROC score is {auroc}, MRR is {mrr}')





