from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_crear_cliente():
    response = client.post("/clientes/", json={
        "nombre": "Simon",
        "ingreso_mensual": 5000,
        "puntaje_crediticio": 780,
        "deuda_actual": 1000
    })

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Simon"
    assert data["puntaje_crediticio"] == 780


def test_listar_clientes():
    # Primero crear un par de clientes
    client.post("/clientes/", json={
        "nombre": "Ana",
        "ingreso_mensual": 6000,
        "puntaje_crediticio": 750,
        "deuda_actual": 500
    })
    
    client.post("/clientes/", json={
        "nombre": "Juan",
        "ingreso_mensual": 7000,
        "puntaje_crediticio": 800,
        "deuda_actual": 300
    })

    response = client.get("/clientes/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_obtener_cliente():
    # Crear un cliente
    cliente_creado = client.post("/clientes/", json={
        "nombre": "María",
        "ingreso_mensual": 5500,
        "puntaje_crediticio": 720,
        "deuda_actual": 800
    }).json()

    # Obtener el cliente por ID
    response = client.get(f"/clientes/{cliente_creado['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "María"
    assert data["id"] == cliente_creado["id"]


def test_obtener_cliente_no_existente():
    response = client.get("/clientes/999999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"


def test_actualizar_cliente():
    # Crear un cliente
    cliente_creado = client.post("/clientes/", json={
        "nombre": "Pedro",
        "ingreso_mensual": 4500,
        "puntaje_crediticio": 680,
        "deuda_actual": 1200
    }).json()

    # Actualizar el cliente
    response = client.put(f"/clientes/{cliente_creado['id']}", json={
        "ingreso_mensual": 5500,
        "puntaje_crediticio": 720
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["ingreso_mensual"] == 5500
    assert data["puntaje_crediticio"] == 720
    assert data["nombre"] == "Pedro"  # No debe cambiar


def test_actualizar_cliente_no_existente():
    response = client.put("/clientes/999999", json={
        "ingreso_mensual": 6000
    })
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"


def test_eliminar_cliente():
    # Crear un cliente
    cliente_creado = client.post("/clientes/", json={
        "nombre": "Luis",
        "ingreso_mensual": 5000,
        "puntaje_crediticio": 700,
        "deuda_actual": 600
    }).json()

    # Eliminar el cliente
    response = client.delete(f"/clientes/{cliente_creado['id']}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Cliente eliminado correctamente"
    
    # Verificar que ya no existe
    response_get = client.get(f"/clientes/{cliente_creado['id']}")
    assert response_get.status_code == 404


def test_eliminar_cliente_no_existente():
    response = client.delete("/clientes/999999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"