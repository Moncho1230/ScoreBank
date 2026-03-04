from pydantic import BaseModel, Field
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    ingreso_mensual: float = Field(..., gt=0)
    puntaje_crediticio: int = Field(..., ge=300, le=850)
    deuda_actual: float = Field(..., ge=0)


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    ingreso_mensual: Optional[float] = Field(None, gt=0)
    puntaje_crediticio: Optional[int] = Field(None, ge=300, le=850)
    deuda_actual: Optional[float] = Field(None, ge=0)


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True