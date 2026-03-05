from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_evaluacion_aprobada():
    cliente = client.post("/clientes/", json={
        "nombre": "Carlos",
        "ingreso_mensual": 8000,
        "puntaje_crediticio": 800,
        "deuda_actual": 500
    }).json()

    solicitud = client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 15000,
        "plazo_meses": 36
    }).json()

    response = client.post(f"/evaluaciones/{solicitud['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["decision"] in ["APROBADO", "APROBADO_CON_CONDICIONES"]


def test_rechazo_por_score_bajo():
    cliente = client.post("/clientes/", json={
        "nombre": "Pedro",
        "ingreso_mensual": 6000,
        "puntaje_crediticio": 550,
        "deuda_actual": 500
    }).json()

    solicitud = client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 8000,
        "plazo_meses": 24
    }).json()

    response = client.post(f"/evaluaciones/{solicitud['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "RECHAZADO"
    assert data["razon"] == "Puntaje crediticio bajo"


def test_rechazo_por_endeudamiento():
    cliente = client.post("/clientes/", json={
        "nombre": "Laura",
        "ingreso_mensual": 4000,
        "puntaje_crediticio": 720,
        "deuda_actual": 2500
    }).json()

    solicitud = client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 5000,
        "plazo_meses": 36
    }).json()

    response = client.post(f"/evaluaciones/{solicitud['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "RECHAZADO"
    assert data["razon"] == "Alto nivel de endeudamiento"


def test_evaluacion_solicitud_no_existe():
    response = client.post("/evaluaciones/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitud no encontrada"




