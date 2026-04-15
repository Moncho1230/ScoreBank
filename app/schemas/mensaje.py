from pydantic import BaseModel
from typing import Optional, Any
from app.schemas.cliente import ClienteResponse


class MensajeDTO(BaseModel):
    cliente: ClienteResponse
    podcast_id: Optional[Any] = None
    vehicle_id: Optional[Any] = None