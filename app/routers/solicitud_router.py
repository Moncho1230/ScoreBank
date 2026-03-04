from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.solicitud import SolicitudCredito
from app.models.cliente import Cliente
from app.schemas.solicitud import (
    SolicitudCreate,
    SolicitudResponse
)

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])



@router.post("/", response_model=SolicitudResponse)
def crear_solicitud(solicitud: SolicitudCreate, db: Session = Depends(get_db)):

    
    cliente = db.query(Cliente).filter(
        Cliente.id == solicitud.cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    nueva_solicitud = SolicitudCredito(
        cliente_id=solicitud.cliente_id,
        monto_solicitado=solicitud.monto_solicitado,
        plazo_meses=solicitud.plazo_meses,
        estado="PENDIENTE"
    )

    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)

    return nueva_solicitud



@router.get("/", response_model=List[SolicitudResponse])
def listar_solicitudes(db: Session = Depends(get_db)):

    solicitudes = db.query(SolicitudCredito).all()
    return solicitudes



@router.get("/{solicitud_id}", response_model=SolicitudResponse)
def obtener_solicitud(solicitud_id: int, db: Session = Depends(get_db)):

    solicitud = db.query(SolicitudCredito).filter(
        SolicitudCredito.id == solicitud_id
    ).first()

    if not solicitud:
        raise HTTPException(
            status_code=404,
            detail="Solicitud no encontrada"
        )

    return solicitud



@router.delete("/{solicitud_id}")
def eliminar_solicitud(solicitud_id: int, db: Session = Depends(get_db)):

    solicitud = db.query(SolicitudCredito).filter(
        SolicitudCredito.id == solicitud_id
    ).first()

    if not solicitud:
        raise HTTPException(
            status_code=404,
            detail="Solicitud no encontrada"
        )

    db.delete(solicitud)
    db.commit()

    return {"message": "Solicitud eliminada correctamente"}