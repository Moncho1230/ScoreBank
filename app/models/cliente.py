from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ingreso_mensual = Column(Float, nullable=False)
    puntaje_crediticio = Column(Integer, nullable=False)
    deuda_actual = Column(Float, nullable=False)