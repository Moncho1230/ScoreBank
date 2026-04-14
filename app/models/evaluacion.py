from sqlalchemy import Column, Integer, Numeric, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=False)
    score_calculado = Column(Numeric, nullable=False)
    decision = Column(String, nullable=False)
    razon = Column(Text, nullable=True)
    fecha_evaluacion = Column(DateTime, server_default=func.now())