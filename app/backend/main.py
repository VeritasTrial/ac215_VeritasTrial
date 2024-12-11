"""Entrypoint of the backend APIs."""

import json
import logging
import os
import time
from contextlib import asynccontextmanager

import chromadb
import chromadb.api
import vertexai  # type: ignore
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from FlagEmbedding import FlagModel  # type: ignore
from vertexai.generative_models import (  # type: ignore
    ChatSession,
    Content,
    GenerativeModel,
    Part,
)

from localtyping import (
    APIChatPayloadType,
    APIChatResponseType,
    APIHeartbeatResponseType,
    APIMetaResponseType,
    APIRetrieveResponseType,
    ModelType,
    TrialFilters,
)
from utils import (
    construct_filters,
    format_exc_details,
    get_metadata_from_id,
    post_filter,
)

logger = logging.getLogger("uvicorn.error")

FRONTEND_URL = os.getenv("FRONTEND_URL")
CHROMADB_HOST = os.getenv("CHROMADB_HOST", "localhost")
SERVER_ROOT_PATH = os.getenv("SERVER_ROOT_PATH", "")
CHROMADB_COLLECTION_NAME = "veritas-trial-embeddings"
GCP_PROJECT_ID = "veritastrial"
GCP_PROJECT_LOCATION = "us-central1"

GH_URL = "https://raw.githubusercontent.com/VeritasTrial/ac215_VeritasTrial/main"
LOGO_URL = f"{GH_URL}/app/frontend/public/veritastrial-wide.png"

# Global states for the FastAPI app
EMBEDDING_MODEL: FlagModel | None = None
CHROMADB_CLIENT: chromadb.api.ClientAPI | None = None
CHAT_SESSIONS: dict[str, ChatSession] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """Context manager to handle the lifespan of the FastAPI app."""
    global EMBEDDING_MODEL, CHROMADB_CLIENT
    EMBEDDING_MODEL = FlagModel("BAAI/bge-small-en-v1.5", use_fp16=True)
    CHROMADB_CLIENT = chromadb.HttpClient(host=CHROMADB_HOST, port=8000)
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_PROJECT_LOCATION)

    yield

    EMBEDDING_MODEL = None
    CHROMADB_CLIENT = None
    CHAT_SESSIONS.clear()


# Initialize the FastAPI app
app = FastAPI(
    lifespan=lifespan,
    root_path=SERVER_ROOT_PATH,
    docs_url=None,
    redoc_url="/",
)

# Handle cross-origin requests from the frontend
if FRONTEND_URL is not None:
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
    openapi_schema["info"]["x-logo"] = {"url": LOGO_URL}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.exception_handler(Exception)
async def custom_exception_handler(
    request: Request, exc: Exception
):  # pragma: no cover
    """Custom handle for all types of exceptions."""
    response = JSONResponse(
        status_code=500,
        content={"details": format_exc_details(exc)},
    )
    if FRONTEND_URL is not None:
        # Manually set the CORS headers for the error response
        response.headers["Access-Control-Allow-Origin"] = FRONTEND_URL
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.get("/heartbeat")
async def heartbeat() -> APIHeartbeatResponseType:
    """Get the current timestamp in nanoseconds."""
    return {"timestamp": time.time_ns()}


@app.get("/retrieve")
async def retrieve(
    query: str, top_k: int, filters_serialized: str
) -> APIRetrieveResponseType:
    """Retrieve items from the ChromaDB collection."""
    if EMBEDDING_MODEL is None:
        raise RuntimeError("Embedding model not initialized")
    if CHROMADB_CLIENT is None:
        raise RuntimeError("ChromaDB not reachable")

    if top_k <= 0 or top_k > 30:
        raise HTTPException(status_code=404, detail="Required 0 < top_k <= 30")

    # Construct the filters; we will need to include the full metadata in the query
    # results if post-filtering is needed, otherwise only documents are needed; TODO:
    # we should avoid post-processing filters if possible
    filters: TrialFilters = json.loads(filters_serialized)
    needs_post_filter, where = construct_filters(filters)
    include = [chromadb.api.types.IncludeEnum("documents")]
    if needs_post_filter:
        include.append(chromadb.api.types.IncludeEnum("metadatas"))

    # Embed the query and query the collection
    query_embedding = EMBEDDING_MODEL.encode(query)
    collection = CHROMADB_CLIENT.get_collection(CHROMADB_COLLECTION_NAME)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=include,
        where=where,
    )

    # Post-filter the results if needed
    if needs_post_filter:
        return post_filter(results, filters)

    # Retrieve the results as is
    ids = results["ids"][0]
    assert results["documents"] is not None, "Missing documents in query results"
    return {"ids": ids, "documents": results["documents"][0]}


@app.get("/meta/{item_id}")
async def meta(item_id: str) -> APIMetaResponseType:
    """Retrieve metadata for a specific item."""
    if CHROMADB_CLIENT is None:
        raise RuntimeError("ChromaDB not reachable")

    collection = CHROMADB_CLIENT.get_collection(CHROMADB_COLLECTION_NAME)
    metadata = get_metadata_from_id(collection, item_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Trial metadata not found")

    return {"metadata": metadata}


@app.post("/chat/{model}/{item_id}")
async def chat(
    model: ModelType, item_id: str, payload: APIChatPayloadType
) -> APIChatResponseType:
    """Chat with a generative model about a specific item."""
    if CHROMADB_CLIENT is None:
        raise RuntimeError("ChromaDB not reachable")

    collection = CHROMADB_CLIENT.get_collection(CHROMADB_COLLECTION_NAME)
    metadata = get_metadata_from_id(collection, item_id)
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

    # Initialize or retrieve the chat session
    session_key = f"{model}-{item_id}"
    if session_key not in CHAT_SESSIONS:
        system_instruction = (
            "You are assisting with a specific clinical trial. You will be given some "
            "information of the clinical trial and asked several questions. Here is "
            "the information of the clinical trial:\n\n"
            f"{json.dumps(metadata, indent=2)}"
        )

        # Create a new chat session
        gen_model = GenerativeModel(
            model_name=model_name,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.75,
                "top_p": 0.95,
            },
            system_instruction=system_instruction,
        )
        chat_session = ChatSession(model=gen_model, history=[])
        CHAT_SESSIONS[session_key] = chat_session
        logger.info(f"Created new chat session: {session_key}")
    else:
        chat_session = CHAT_SESSIONS[session_key]

    # Add the user's query to the chat session
    user_message = Content(role="user", parts=[Part.from_text(payload.query)])
    chat_session.history.append(user_message)

    # Generate the response and add to the chat session
    response = chat_session.send_message(payload.query)
    response_text = response.text.strip()
    chat_session.history.append(
        Content(role="model", parts=[Part.from_text(response_text)])
    )

    return {"response": response_text}
