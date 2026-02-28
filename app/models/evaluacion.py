from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"))
    score_calculado = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    razon = Column(String, nullable=True)

    solicitud = relationship("SolicitudCredito")