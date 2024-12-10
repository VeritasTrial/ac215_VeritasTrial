"""Entrypoint of the backend APIs."""

import json
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from itertools import permutations

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
from utils import format_exc_details, get_metadata_from_id

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


def filter_by_date(results_full, date_key, from_date, to_date):
    filtered_documents = []
    filtered_ids = []

    metadata = results_full["metadatas"][0]
    documents = results_full["documents"][0]
    ids = results_full["ids"][0]

    for idx, meta in enumerate(metadata):
        try:
            date_str = meta.get(date_key)
            if date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if from_date <= date_obj <= to_date:
                    filtered_documents.append(documents[idx])
                    filtered_ids.append(ids[idx])
        except (ValueError, KeyError) as e:
            print(f"Error processing metadata: {meta}. Error: {e}")

    return {"ids": [filtered_ids], "documents": [filtered_documents]}


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

    # Construct the filters
    filters: TrialFilters = json.loads(filters_serialized)
    processed_filters = []

    if "studyType" in filters:
        if filters["studyType"] == "interventional":
            processed_filters.append({"study_type": "INTERVENTIONAL"})
        elif filters["studyType"] == "observational":
            processed_filters.append({"study_type": "OBSERVATIONAL"})

    if "acceptsHealthy" in filters and not filters["acceptsHealthy"]:
        # NOTE: If this filter is True, it means to accept healthy participants,
        # and unhealthy participants are always accepted so it is equivalent to
        # not having this filter at all
        processed_filters.append({"accepts_healthy": False})  # type: ignore  # TODO: Fix this

    if "eligibleSex" in filters:
        if filters["eligibleSex"] == "female":
            processed_filters.append({"eligible_sex": "FEMALE"})
        elif filters["eligibleSex"] == "male":
            processed_filters.append({"eligible_sex": "MALE"})

    # TODO: Change this to a post-filter
    if "studyPhases" in filters and len(filters["studyPhases"]) > 0:
        # NOTE: ChromaDB does not support the $contains operator on strings for
        # metadata fields. Therefore, we need to generate all possible
        # combinations and do exact matching
        all_phases = ["EARLY_PHASE1", "PHASE1", "PHASE2", "PHASE3", "PHASE4"]
        possible_values = []
        for r in range(len(all_phases)):
            for combo in permutations(all_phases, r + 1):
                if any(phase in combo for phase in filters["studyPhases"]):
                    possible_values.append(", ".join(combo))
        processed_filters.append({"study_phases": {"$in": possible_values}})  # type: ignore  # TODO: Fix this

    if "ageRange" in filters:
        # NOTE: We want the age range to intersect with the desired range
        min_age, max_age = filters["ageRange"]
        processed_filters.append({"min_age": {"$lte": max_age}})  # type: ignore  # TODO: Fix this
        processed_filters.append({"max_age": {"$gte": min_age}})  # type: ignore  # TODO: Fix this

    # Construct the where clause
    where: chromadb.Where | None
    if len(processed_filters) == 0:
        where = None
    elif len(processed_filters) == 1:
        where = processed_filters[0]  # type: ignore  # TODO: Fix this
    else:
        where = {"$and": processed_filters}  # type: ignore  # TODO: Fix this

    # Embed the query and query the collection
    query_embedding = EMBEDDING_MODEL.encode(query)
    collection = CHROMADB_CLIENT.get_collection(CHROMADB_COLLECTION_NAME)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[chromadb.api.types.IncludeEnum("documents")],
        where=where,
    )

    results_full = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            chromadb.api.types.IncludeEnum("documents"),
            chromadb.api.types.IncludeEnum("metadatas"),
        ],
        where=where,
    )

    if "lastUpdateDatePosted" in filters:
        from_timestamp, to_timestamp = filters["lastUpdateDatePosted"]
        from_date = datetime.fromtimestamp(from_timestamp / 1000)
        to_date = datetime.fromtimestamp(to_timestamp / 1000)
        results = filter_by_date(
            results_full, "last_update_date_posted", from_date, to_date
        )

    if "resultsDatePosted" in filters:
        from_timestamp, to_timestamp = filters["resultsDatePosted"]
        from_date = datetime.fromtimestamp(from_timestamp / 1000)
        to_date = datetime.fromtimestamp(to_timestamp / 1000)
        results = filter_by_date(
            results_full, "results_date_posted", from_date, to_date
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
