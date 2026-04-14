from sqlalchemy import Column, Integer, String, Float, Numeric, DateTime
from sqlalchemy.sql import func
from app.db import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ingreso_mensual = Column(Numeric, nullable=False)
    puntaje_crediticio = Column(Integer, nullable=False)
    deuda_actual = Column(Numeric, nullable=False)
    created_at = Column(DateTime, server_default=func.now())