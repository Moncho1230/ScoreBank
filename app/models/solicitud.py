from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base

class SolicitudCredito(Base):
    __tablename__ = "solicitudes_credito"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    monto_solicitado = Column(Numeric, nullable=False)
    plazo_meses = Column(Integer, nullable=False)
    estado = Column(String, nullable=False, default="PENDIENTE")
    tasa_interes = Column(Numeric, nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now())