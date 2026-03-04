from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EvaluacionBase(BaseModel):
    solicitud_id: int
    score_calculado: float
    decision: str
    razon: Optional[str] = None


class EvaluacionCreate(EvaluacionBase):
    pass


class EvaluacionResponse(EvaluacionBase):
    id: int
    fecha_evaluacion: datetime

    class Config:
        from_attributes = True