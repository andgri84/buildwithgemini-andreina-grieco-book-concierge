"""FastAPI proxy per l'agente Andreina Grieco Book Concierge con A2A e catalog API."""

import os
import uuid
import datetime
from typing import Optional

import google.auth
import google.auth.transport.requests
import httpx
from google.cloud import firestore
from a2a.client import ClientConfig, ClientFactory
from a2a.types import (
    AgentCard,
    FilePart,
    Message,
    Part,
    Role,
    TaskArtifactUpdateEvent,
    TextPart,
    TransportProtocol,
)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

RESOURCE = os.environ.get(
    "AGENT_ENGINE_RESOURCE_NAME",
    "projects/536969637446/locations/us-east1/reasoningEngines/6346054560569622528"
)
AGENT_DIRECTORY = os.environ.get("AGENT_DIRECTORY", "app")
LOCATION = RESOURCE.split("/locations/")[1].split("/")[0]

A2A_BASE = (
    f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/"
    f"{RESOURCE}/api/a2a/{AGENT_DIRECTORY}"
)
A2A_CARD_URL = f"{A2A_BASE}/.well-known/agent-card.json"
_A2UI_MIME = "application/json+a2ui"

PROJECT_ID = "qwiklabs-gcp-03-9513a337097b"
_db: Optional[firestore.Client] = None

def get_db():
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db

_creds, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

def _auth_headers() -> dict[str, str]:
    _creds.refresh(google.auth.transport.requests.Request())
    return {
        "Authorization": f"Bearer {_creds.token}",
        "Content-Type": "application/json",
    }

app = FastAPI()

@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )

_contexts: dict[str, str] = {}
_card: AgentCard | None = None

async def _get_card(client: httpx.AsyncClient) -> AgentCard:
    global _card
    if _card is None:
        resp = await client.get(A2A_CARD_URL)
        resp.raise_for_status()
        card = AgentCard(**resp.json())
        card.url = A2A_BASE
        _card = card
    return _card

def _extract_parts(parts: list) -> list[dict]:
    out: list[dict] = []
    for p in parts:
        root = getattr(p, "root", p)
        if isinstance(root, TextPart) and getattr(root, "text", None):
            out.append({"kind": "text", "text": root.text})
        elif getattr(root, "data", None) is not None:
            meta = getattr(root, "metadata", None) or {}
            mime = meta.get("mimeType") if isinstance(meta, dict) else None
            if mime == _A2UI_MIME:
                out.append({"kind": "a2ui", "data": root.data})
        elif isinstance(root, FilePart):
            uri = getattr(getattr(root, "file", None), "uri", None)
            if uri:
                out.append({"kind": "text", "text": uri})
    return out

@app.get("/api/catalog")
async def get_catalog():
    """Restituisce libri e box direttamente da Firestore."""
    db = get_db()
    
    books = []
    for doc in db.collection("catalog_books").stream():
        books.append(doc.to_dict())
        
    boxes = []
    for doc in db.collection("catalog_boxes").stream():
        boxes.append(doc.to_dict())
        
    return JSONResponse({"books": books, "boxes": boxes})

@app.post("/api/order")
async def create_order(req: Request):
    """Registra direttamente un ordine su Firestore."""
    data = await req.json()
    order_id = f"AG-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    order_record = {
        "order_id": order_id,
        "created_at": timestamp,
        "customer_name": data.get("customer_name", ""),
        "dedication_name": data.get("dedication_name", ""),
        "box_id": data.get("box_id", ""),
        "box_name": data.get("box_name", ""),
        "shipping_address": data.get("shipping_address", ""),
        "shipping_method": data.get("shipping_method", "Poste Non Tracciato"),
        "customer_contact": data.get("customer_contact", ""),
        "payment_choice": data.get("payment_choice", "Da confermare"),
        "notes": data.get("notes", ""),
        "total_price": data.get("total_price", 0.0),
        "status": "In attesa di pagamento/finalizzazione",
    }
    
    db = get_db()
    db.collection("book_orders").document(order_id).set(order_record)
    
    return JSONResponse({
        "status": "success",
        "order_id": order_id,
        "order": order_record,
        "author_contacts": {
            "instagram": "@andreina_grieco_autrice",
            "vinted": "andreinagrieco_libri",
            "email": "andreina.grieco.autrice@gmail.com",
            "paypal": "paypal.me/andreinagrieco"
        }
    })

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "")
    user_id = body.get("user_id") or "web-user"
    parts: list[dict] = []

    async with httpx.AsyncClient(headers=_auth_headers(), timeout=120) as client:
        card = await _get_card(client)
        factory = ClientFactory(
            ClientConfig(
                supported_transports=[
                    TransportProtocol.jsonrpc,
                    TransportProtocol.http_json,
                ],
                httpx_client=client,
            )
        )
        a2a_client = factory.create(card)

        msg = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[Part(root=TextPart(text=message))],
            context_id=_contexts.get(user_id),
        )

        last_task = None
        got_artifact_update = False
        async for event in a2a_client.send_message(msg):
            if not isinstance(event, tuple):
                continue
            task, update = event
            if task is not None:
                last_task = task
                if getattr(task, "context_id", None):
                    _contexts[user_id] = task.context_id
            if isinstance(update, TaskArtifactUpdateEvent):
                got_artifact_update = True
                parts.extend(_extract_parts(update.artifact.parts))

        if not got_artifact_update and last_task is not None:
            for artifact in getattr(last_task, "artifacts", None) or []:
                parts.extend(_extract_parts(artifact.parts))

    if not parts:
        parts = [{"kind": "text", "text": "(The agent didn't return a reply.)"}]
    return JSONResponse({"parts": parts})

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
