from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SolicitudBase(BaseModel):
    cliente_id: int
    monto_solicitado: float = Field(..., gt=0)
    plazo_meses: int = Field(..., gt=0)


class SolicitudCreate(SolicitudBase):
    pass


class SolicitudUpdate(BaseModel):
    estado: Optional[str] = None
    tasa_interes: Optional[float] = None


class SolicitudResponse(SolicitudBase):
    id: int
    estado: str
    tasa_interes: Optional[float]
    fecha_creacion: datetime

    class Config:
        from_attributes = True