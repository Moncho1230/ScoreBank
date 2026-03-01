from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import (
    ClienteCreate,
    ClienteResponse,
    ClienteUpdate
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


CLIENTE_NO_ENCONTRADO = "Cliente no encontrado"

@router.post("/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):

    nuevo_cliente = Cliente(**cliente.dict())

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):

    clientes = db.query(Cliente).all()
    return clientes


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):

    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)

    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, datos: ClienteUpdate, db: Session = Depends(get_db)):

    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)

    return cliente


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):

    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)

    db.delete(cliente)
    db.commit()

    return {"message": "Cliente eliminado correctamente"}