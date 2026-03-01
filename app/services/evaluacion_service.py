from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.solicitud import Solicitud
from app.models.cliente import Cliente
from app.models.evaluacion import Evaluacion


def calcular_score(cliente: Cliente, solicitud: Solicitud) -> int:
    score = 500

    if cliente.ingresos_mensuales > 3000000:
        score += 100

    if solicitud.monto_solicitado < cliente.ingresos_mensuales * 5:
        score += 100

    if solicitud.plazo_meses <= 24:
        score += 50

    return score


def evaluar_solicitud(solicitud_id: int, db: Session):
    solicitud = db.query(Solicitud).filter(
        Solicitud.id == solicitud_id
    ).first()

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    cliente = db.query(Cliente).filter(
        Cliente.id == solicitud.cliente_id
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    score = calcular_score(cliente, solicitud)

    decision = "APROBADO" if score >= 650 else "RECHAZADO"

    nueva_evaluacion = Evaluacion(
        solicitud_id=solicitud.id,
        score_calculado=score,
        decision=decision,
        observaciones="Evaluación automática generada por el sistema"
    )

    solicitud.estado = decision

    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)

    return nueva_evaluacion