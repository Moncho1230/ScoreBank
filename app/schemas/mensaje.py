from pydantic import BaseModel
from typing import Optional, Any
from app.schemas.cliente import ClienteResponse


class MensajeDTO(BaseModel):
    cliente: ClienteResponse
    podcast: Optional[Any] = None
    vehiculo: Optional[Any] = None 