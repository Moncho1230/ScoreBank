from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.solicitud import SolicitudCredito
from app.models.cliente import Cliente
from app.models.evaluacion import Evaluacion


def evaluar_solicitud(solicitud_id: int, db: Session):

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

    # 🔹 Calcular nivel de endeudamiento real
    if cliente.ingreso_mensual == 0:
        raise HTTPException(status_code=400, detail="Ingreso mensual inválido")

    nivel_endeudamiento = cliente.deuda_actual / cliente.ingreso_mensual

    # 🔹 Reglas de decisión
    if cliente.puntaje_crediticio < 600:
        decision = "RECHAZADO"
        razon = "Puntaje crediticio bajo"
        tasa = None

    elif nivel_endeudamiento > 0.4:
        decision = "RECHAZADO"
        razon = "Alto nivel de endeudamiento"
        tasa = None

    elif cliente.puntaje_crediticio > 750 and nivel_endeudamiento < 0.2:
        decision = "APROBADO"
        razon = "Cliente con perfil preferencial"
        tasa = 0.08

    else:
        decision = "APROBADO_CON_CONDICIONES"
        razon = "Aprobado con tasa estándar"
        tasa = 0.12

    nueva_evaluacion = Evaluacion(
        solicitud_id=solicitud.id,
        score_calculado=cliente.puntaje_crediticio,
        decision=decision,
        razon=razon
    )

    solicitud.estado = decision
    solicitud.tasa_interes = tasa

    db.add(nueva_evaluacion)
    db.commit()
    db.refresh(nueva_evaluacion)

    return nueva_evaluacion