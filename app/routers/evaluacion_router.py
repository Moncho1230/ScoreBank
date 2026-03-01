from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.evaluacion import Evaluacion
from app.models.solicitud import SolicitudCredito
from app.models.cliente import Cliente
from app.schemas.evaluacion import EvaluacionResponse

router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones"])


@router.post("/{solicitud_id}", response_model=EvaluacionResponse)
def evaluar_solicitud(solicitud_id: int, db: Session = Depends(get_db)):

    solicitud = db.query(SolicitudCredito).filter(
        SolicitudCredito.id == solicitud_id
    ).first()

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    cliente = db.query(Cliente).filter(
        Cliente.id == solicitud.cliente_id
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    
    nivel_endeudamiento = cliente.deuda_actual / cliente.ingreso_mensual
    score = cliente.puntaje_crediticio - (nivel_endeudamiento * 100)

    decision = ""
    razon = ""
    tasa = None

    
    if cliente.puntaje_crediticio < 600:
        decision = "RECHAZADO"
        razon = "Puntaje crediticio bajo"
        solicitud.estado = "RECHAZADO"

    elif nivel_endeudamiento > 0.4:
        decision = "RECHAZADO"
        razon = "Alto nivel de endeudamiento"
        solicitud.estado = "RECHAZADO"

    elif cliente.puntaje_crediticio > 750 and nivel_endeudamiento < 0.2:
        decision = "APROBADO"
        razon = "Cliente preferencial"
        tasa = 8.5
        solicitud.estado = "APROBADO"
        solicitud.tasa_interes = tasa

    else:
        decision = "APROBADO_CON_CONDICIONES"
        razon = "Perfil medio"
        tasa = 12.0
        solicitud.estado = "APROBADO"
        solicitud.tasa_interes = tasa

    
    nueva_evaluacion = Evaluacion(
        solicitud_id=solicitud.id,
        score_calculado=round(score, 2),
        decision=decision,
        razon=razon
    )

    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)

    return nueva_evaluacion