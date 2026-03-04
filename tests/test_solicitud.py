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


def test_crear_solicitud_cliente_no_existe():
    response = client.post("/solicitudes/", json={
        "cliente_id": 999999,
        "monto_solicitado": 10000,
        "plazo_meses": 24
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"


def test_listar_solicitudes():
    # Crear cliente
    cliente = client.post("/clientes/", json={
        "nombre": "Roberto",
        "ingreso_mensual": 5000,
        "puntaje_crediticio": 740,
        "deuda_actual": 600
    }).json()

    # Crear un par de solicitudes
    client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 8000,
        "plazo_meses": 12
    })
    
    client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 15000,
        "plazo_meses": 36
    })

    response = client.get("/solicitudes/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_obtener_solicitud():
    # Crear cliente
    cliente = client.post("/clientes/", json={
        "nombre": "Carolina",
        "ingreso_mensual": 6000,
        "puntaje_crediticio": 760,
        "deuda_actual": 400
    }).json()

    # Crear solicitud
    solicitud_creada = client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 12000,
        "plazo_meses": 24
    }).json()

    # Obtener solicitud por ID
    response = client.get(f"/solicitudes/{solicitud_creada['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == solicitud_creada["id"]
    assert data["monto_solicitado"] == 12000


def test_obtener_solicitud_no_existente():
    response = client.get("/solicitudes/999999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitud no encontrada"


def test_eliminar_solicitud():
    # Crear cliente
    cliente = client.post("/clientes/", json={
        "nombre": "Diego",
        "ingreso_mensual": 5500,
        "puntaje_crediticio": 730,
        "deuda_actual": 700
    }).json()

    # Crear solicitud
    solicitud_creada = client.post("/solicitudes/", json={
        "cliente_id": cliente["id"],
        "monto_solicitado": 9000,
        "plazo_meses": 18
    }).json()

    # Eliminar la solicitud
    response = client.delete(f"/solicitudes/{solicitud_creada['id']}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Solicitud eliminada correctamente"
    
    # Verificar que ya no existe
    response_get = client.get(f"/solicitudes/{solicitud_creada['id']}")
    assert response_get.status_code == 404


def test_eliminar_solicitud_no_existente():
    response = client.delete("/solicitudes/999999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Solicitud no encontrada"