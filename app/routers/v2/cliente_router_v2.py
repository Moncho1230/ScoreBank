# app/routers/v2/cliente_router_v2.py
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated
import os

from app.db import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.schemas.mensaje import MensajeDTO

router = APIRouter(prefix="/clientes", tags=["Clientes v2"])

CLIENTE_NO_ENCONTRADO = "Cliente no encontrado"
API2_URL = os.getenv("API2_URL", "--- IGNORE ---")


@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Annotated[Session, Depends(get_db)]):
    nuevo = Cliente(**cliente.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Annotated[Session, Depends(get_db)]):
    return db.query(Cliente).all()


@router.get("/{cliente_id}", response_model=ClienteResponse, responses={404: {"description": CLIENTE_NO_ENCONTRADO}})
def obtener_cliente(cliente_id: int, db: Annotated[Session, Depends(get_db)]):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse, responses={404: {"description": CLIENTE_NO_ENCONTRADO}})
def put_cliente(cliente_id: int, datos: ClienteUpdate, db: Annotated[Session, Depends(get_db)]):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse, responses={404: {"description": CLIENTE_NO_ENCONTRADO}})
def patch_cliente(cliente_id: int, datos: ClienteUpdate, db: Annotated[Session, Depends(get_db)]):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}", responses={404: {"description": CLIENTE_NO_ENCONTRADO}})
def eliminar_cliente(cliente_id: int, db: Annotated[Session, Depends(get_db)]):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente eliminado correctamente"}


# Flujo encadenado

@router.post("/procesar/{cliente_id}", response_model=MensajeDTO, responses={404: {"description": CLIENTE_NO_ENCONTRADO}, 502: {"description": "Error en API #2"}, 503: {"description": "API #2 no disponible"}})
async def iniciar_flujo(cliente_id: int, db: Annotated[Session, Depends(get_db)]):
    
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=CLIENTE_NO_ENCONTRADO)


    mensaje = MensajeDTO(cliente=ClienteResponse.from_orm(cliente))

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{API2_URL}/api/v2/podcasts/procesar",
                json=mensaje.dict()
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Error en API #2: {e.response.status_code}"
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=503,
                detail="API #2 no disponible"
            )

    
    return response.json()