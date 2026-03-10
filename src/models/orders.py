#modelo de exito para la respuesta de creación de orden
from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from typing import Literal

AllowedStatus = Literal["CREATED", "PENDING"]

class CreateOrderResponse(BaseModel):
    id: str = Field(min_length=1)
    status: AllowedStatus
    total: float
    currency: str = Field(min_length=1)
    created_at: datetime

    @field_validator("total")
    @classmethod
    def total_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("total must be > 0")
        return v