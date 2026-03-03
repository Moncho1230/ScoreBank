from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_crear_cliente():
    response = client.post("/clientes/", json={
        "nombre": "Simon",
        "ingreso_mensual": -5000,
        "puntaje_crediticio": 780,
        "deuda_actual": 1000
    })

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Simon"
    assert data["puntaje_crediticio"] == 780