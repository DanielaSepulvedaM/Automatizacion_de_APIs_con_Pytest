#modelo de error para la respuesta de error
from pydantic import BaseModel, Field
from typing import List


class ErrorDetail(BaseModel):
    field: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class ErrorResponse(BaseModel):
    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    details: List[ErrorDetail] = Field(min_length=1)