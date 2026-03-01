from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.evaluacion_service import evaluar_solicitud

router = APIRouter(
    prefix="/evaluaciones",
    tags=["Evaluaciones"]
)


@router.post("/{solicitud_id}")
def evaluar_credito(solicitud_id: int, db: Session = Depends(get_db)):
    return evaluar_solicitud(solicitud_id, db)