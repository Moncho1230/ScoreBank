from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_crear_solicitud():
    # Crear cliente primero
    cliente = client.post("/clientes/", json={
        "nombre": "Laura",
        "ingreso_mensual": 4000,
        "puntaje_crediticio": 720,
        "deuda_actual": 500
    }).json()

    response = client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 10000,
        "plazo_meses": 24
    })

    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "PENDIENTE"