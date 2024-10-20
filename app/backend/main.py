import json

import chromadb
import vertexai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from FlagEmbedding import FlagModel
from vertexai.generative_models import GenerativeModel

EMBEDDING_MODEL = FlagModel("BAAI/bge-small-en-v1.5", use_fp16=True)
CHROMADB_CLIENT = chromadb.HttpClient(host="chromadb", port=8000)
CHROMADB_COLLECTION = CHROMADB_CLIENT.get_collection("veritas-trial-embeddings")

GCP_PROJECT_ID = "veritastrial"
GCP_PROJECT_LOCATION = "us-central1"
vertexai.init(project=GCP_PROJECT_ID, location=GCP_PROJECT_LOCATION)

app = FastAPI()

# Handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Default port of Vite development server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/heartbeat")
def heartbeat():
    """Health check endpoint."""
    return {"status": "alive"}


@app.get("/query")
def query(query, top_k=5, get_documents=False, get_metadatas=False):
    """Query the ChromaDB collection."""
    query_include = []
    if get_documents:
        query_include.append("documents")
    if get_metadatas:
        query_include.append("metadatas")

    query_embedding = EMBEDDING_MODEL.encode(query)
    results = CHROMADB_COLLECTION.query(
        query_embeddings=[query_embedding],
        n_results=int(top_k),
        include=query_include,
    )

    cleaned_results = {"ids": results["ids"][0]}

    if get_documents:
        cleaned_results["documents"] = results["documents"][0]

    if get_metadatas:
        cleaned_metadatas = []
        for metadata in results["metadatas"][0]:
            metadata["collaborators"] = json.loads(metadata["collaborators"])
            metadata["conditions"] = json.loads(metadata["conditions"])
            metadata["documents"] = json.loads(metadata["documents"])
            metadata["Interventions"] = json.loads(
                metadata["Interventions"]
            )  # TODO: case
            metadata["locations"] = json.loads(metadata["locations"])
            metadata["officials"] = json.loads(metadata["officials"])
            metadata["other_measure_outcomes"] = json.loads(
                metadata["other_measure_outcomes"]
            )
            metadata["primary_measure_outcomes"] = json.loads(
                metadata["primary_measure_outcomes"]
            )
            metadata["references"] = json.loads(metadata["references"])
            metadata["secondary_measure_outcomes"] = json.loads(
                metadata["secondary_measure_outcomes"]
            )
            cleaned_metadatas.append(metadata)
        cleaned_results["metadatas"] = cleaned_metadatas

    return cleaned_results


@app.get("/generate")
def generate(query, endpoint="6894888983713546240"):
    """Generate a response from the model."""
    model = GenerativeModel(
        f"projects/{GCP_PROJECT_ID}/locations/{GCP_PROJECT_LOCATION}/endpoints/{endpoint}",
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.75,
            "top_p": 0.95,
        },
    )

    response = model.generate_content(query, stream=False)
    return {"response": response.text.strip()}
