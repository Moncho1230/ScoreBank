from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class SolicitudCredito(Base):
    __tablename__ = "solicitudes_credito"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    monto_solicitado = Column(Float, nullable=False)
    plazo_meses = Column(Integer, nullable=False)
    estado = Column(String, default="PENDIENTE")
    tasa_interes = Column(Float, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente")