#api para simular la creación de órdenes, con validaciones básicas y respuestas de éxito y error
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone
import uuid

app = FastAPI(title="Local Orders API")
UNSTABLE_COUNTER = 0

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/unstable")
def unstable():
    global UNSTABLE_COUNTER
    UNSTABLE_COUNTER += 1

    if UNSTABLE_COUNTER <= 2:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "temporary_error",
                "attempt": UNSTABLE_COUNTER,
            },
        )

    return {
        "status": "ok",
        "attempt": UNSTABLE_COUNTER,
    }

# --------- Models (Request) ----------
class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1)
    qty: int
    price: float  

class CreateOrderIn(BaseModel):
    customer_id: str = Field(min_length=1)
    items: List[OrderItemIn]
    currency: str = Field(min_length=1)

# --------- Helpers ----------
def now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# --------- Endpoint ----------
@app.post("/orders", status_code=201)
def create_order(payload: CreateOrderIn):
    # N1: items vacío => error estándar (opción 2)
    if len(payload.items) == 0:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": "VALIDATION_ERROR",
                "message": "Invalid request",
                "details": [{"field": "items", "reason": "must not be empty"}],
            },
        ) 

    # Validaciones simples (para que tengas base realista)
    for i, item in enumerate(payload.items):
        if item.qty < 1:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request",
                    "details": [{"field": f"items[{i}].qty", "reason": "must be >= 1"}],
                },
            )
        if item.price <= 0:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request",
                    "details": [{"field": f"items[{i}].price", "reason": "must be > 0"}],
                },
            )

    total = sum(item.qty * item.price for item in payload.items)

    # P1: éxito
    return {
        "id": f"ORD-{uuid.uuid4().hex[:8]}",
        "status": "CREATED",
        "total": total,
        "currency": payload.currency,
        "created_at": now_iso(),
    }
