import json
import time
from pathlib import Path

import chromadb
import chromadb.types
import vertexai  # type: ignore
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from FlagEmbedding import FlagModel  # type: ignore
from vertexai.generative_models import GenerativeModel  # type: ignore

from localtyping import (
    APIChatResponseType,
    APIHeartbeatResponseType,
    APIRetrieveResponseType,
    ModelType,
)
from utils import _clean_metadata, _get_metadata_from_id

EMBEDDING_MODEL = FlagModel("BAAI/bge-small-en-v1.5", use_fp16=True)
CHROMADB_CLIENT = chromadb.HttpClient(host="chromadb", port=8000)
CHROMADB_COLLECTION = CHROMADB_CLIENT.get_collection("veritas-trial-embeddings")

GCP_PROJECT_ID = "veritastrial"
GCP_PROJECT_LOCATION = "us-central1"
vertexai.init(project=GCP_PROJECT_ID, location=GCP_PROJECT_LOCATION)

app = FastAPI(docs_url=None, redoc_url="/")

# Handle cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    """OpenAPI schema customization."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="VeritasTrial APIs",
        version="0.0.0",
        description="OpenAPI specification for the VeritasTrial APIs.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        # TODO: Change to the VeritasTrial logo
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore


@app.get("/heartbeat")
async def heartbeat() -> APIHeartbeatResponseType:
    """Get the current timestamp in nanoseconds."""
    return {"timestamp": time.time_ns()}


@app.get("/retrieve")
async def retrieve(
    query: str,
    top_k: int = 3,
    get_documents: bool = False,
    get_metadatas: bool = False,
) -> APIRetrieveResponseType:
    """Retrieve items from the ChromaDB collection."""
    if top_k <= 0 or top_k > 100:
        raise HTTPException(status_code=404, detail="Invalid top_k value")

    include_list: chromadb.Include = []
    if get_documents:
        include_list.append(chromadb.api.types.IncludeEnum("documents"))
    if get_metadatas:
        include_list.append(chromadb.api.types.IncludeEnum("metadatas"))

    # Embed the query and query the collection
    query_embedding = EMBEDDING_MODEL.encode(query)
    results = CHROMADB_COLLECTION.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=include_list,
    )

    # Clean the results
    cleaned_results: APIRetrieveResponseType = {"ids": results["ids"][0]}
    if get_documents and results["documents"] is not None:
        cleaned_results["documents"] = results["documents"][0]
    if get_metadatas and results["metadatas"] is not None:
        cleaned_results["metadatas"] = [
            _clean_metadata(metadata) for metadata in results["metadatas"][0]
        ]
    return cleaned_results


@app.get("/chat/{endpoint}/{item_id}")
async def chat(endpoint: ModelType, item_id: str, query: str) -> APIChatResponseType:
    """Chat with a generative model about a specific item."""
    if endpoint not in ("gemini-1.5-flash-001",):
        model_name = (
            f"projects/{GCP_PROJECT_ID}/locations/{GCP_PROJECT_LOCATION}/"
            f"endpoints/{endpoint}"
        )
    else:
        model_name = endpoint

    # Initialize the generative model
    model = GenerativeModel(
        model_name=model_name,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.75,
            "top_p": 0.95,
        },
    )

    # Extract metadata from the item ID and combine with the query
    metadata = _get_metadata_from_id(CHROMADB_COLLECTION, item_id)
    query = (
        "You will be given the information of a clinical trial and asked a "
        "question. The information is as follows:\n\n"
        f"{json.dumps(metadata, indent=2)}\n\n"
        "## Question\n\n"
        f"{query}"
    )

    # Generate the response
    response = model.generate_content(query, stream=False)
    return {"response": response.text.strip()}
