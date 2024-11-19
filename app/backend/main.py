"""Entrypoint of the backend APIs."""

import json
import os
import time
from contextlib import asynccontextmanager

import chromadb
import vertexai  # type: ignore
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from FlagEmbedding import FlagModel  # type: ignore
from vertexai.generative_models import GenerativeModel  # type: ignore

from localtyping import (
    APIChatResponseType,
    APIHeartbeatResponseType,
    APIMetaResponseType,
    APIRetrieveResponseType,
    ModelType,
)
from utils import format_exc_details, get_metadata_from_id

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")
CHROMADB_COLLECTION_NAME = "veritas-trial-embeddings"
GCP_PROJECT_ID = "veritastrial"
GCP_PROJECT_LOCATION = "us-central1"

# Global states for the FastAPI app
EMBEDDING_MODEL: FlagModel | None = None
CHROMADB_COLLECTION: chromadb.Collection | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """Context manager to handle the lifespan of the FastAPI app."""
    global EMBEDDING_MODEL, CHROMADB_COLLECTION
    EMBEDDING_MODEL = FlagModel("BAAI/bge-small-en-v1.5", use_fp16=True)
    chromadb_client = chromadb.HttpClient(host="chromadb", port=8000)
    CHROMADB_COLLECTION = chromadb_client.get_collection(CHROMADB_COLLECTION_NAME)
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_PROJECT_LOCATION)

    yield

    EMBEDDING_MODEL = None
    CHROMADB_COLLECTION = None


# Initialize the FastAPI app
app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url="/")

# Handle cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():  # pragma: no cover
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


@app.exception_handler(Exception)
async def custom_exception_handler(
    request: Request, exc: Exception
):  # pragma: no cover
    """Custom handle for all types of exceptions."""
    response = JSONResponse(
        status_code=500,
        content={"details": format_exc_details(exc)},
    )
    # Manually set the CORS headers for the error response
    response.headers["Access-Control-Allow-Origin"] = FRONTEND_URL
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.get("/heartbeat")
async def heartbeat() -> APIHeartbeatResponseType:
    """Get the current timestamp in nanoseconds."""
    return {"timestamp": time.time_ns()}


@app.get("/retrieve")
async def retrieve(query: str, top_k: int) -> APIRetrieveResponseType:
    """Retrieve items from the ChromaDB collection."""
    if EMBEDDING_MODEL is None:
        raise RuntimeError("Embedding model not initialized")
    if CHROMADB_COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")

    if top_k <= 0 or top_k > 30:
        raise HTTPException(status_code=404, detail="Required 0 < top_k <= 30")

    # Embed the query and query the collection
    query_embedding = EMBEDDING_MODEL.encode(query)
    results = CHROMADB_COLLECTION.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[chromadb.api.types.IncludeEnum("documents")],
    )

    # Retrieve the results
    ids = results["ids"][0]
    if results["documents"] is not None:
        documents = results["documents"][0]
    else:
        documents = [""] * len(ids)

    return {"ids": ids, "documents": documents}


@app.get("/meta/{item_id}")
async def meta(item_id: str) -> APIMetaResponseType:
    """Retrieve metadata for a specific item."""
    if CHROMADB_COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")

    metadata = get_metadata_from_id(CHROMADB_COLLECTION, item_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Trial metadata not found")

    return {"metadata": metadata}


@app.get("/chat/{model}/{item_id}")
async def chat(model: ModelType, item_id: str, query: str) -> APIChatResponseType:
    """Chat with a generative model about a specific item."""
    if CHROMADB_COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")

    metadata = get_metadata_from_id(CHROMADB_COLLECTION, item_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Trial metadata not found")

    # Determine the model to use
    if model not in ("gemini-1.5-flash-001",):
        model_name = (
            f"projects/{GCP_PROJECT_ID}/locations/{GCP_PROJECT_LOCATION}/"
            f"endpoints/{model}"
        )
    else:
        model_name = model

    # Initialize the generative model
    gen_model = GenerativeModel(
        model_name=model_name,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.75,
            "top_p": 0.95,
        },
    )

    # Combine metadata into the query
    query = (
        "You will be given the information of a clinical trial and asked a "
        "question. The information is as follows:\n\n"
        f"{json.dumps(metadata, indent=2)}\n\n"
        "## Question\n\n"
        f"{query}"
    )

    # Generate the response
    response = gen_model.generate_content(query, stream=False)
    return {"response": response.text.strip()}
