# ScoreBank API 🏦

API REST para evaluación y gestión de créditos bancarios, desplegada en Google Cloud Platform con arquitectura multicloud.

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación local](#instalación-local)
- [Variables de entorno](#variables-de-entorno)
- [Endpoints](#endpoints)
- [Flujo encadenado multicloud](#flujo-encadenado-multicloud)
- [Despliegue en GKE](#despliegue-en-gke)
- [CI/CD con Cloud Build](#cicd-con-cloud-build)
- [Monitoreo](#monitoreo)
- [Versionado](#versionado)

---

## Descripción

ScoreBank API es el primer eslabón de una cadena de microservicios multicloud. Gestiona la entidad **Cliente** con campos financieros como ingreso mensual, puntaje crediticio y deuda actual. Expone endpoints REST en versiones `v1` y `v2`, e inicia el flujo encadenado que atraviesa tres APIs en dos nubes distintas (GCP y AWS).

---

## Arquitectura

![Arquitectura multicloud](docs/arquitectura.png)

```
Cliente HTTP
     │
     ▼
LoadBalancer (GCP · 34.41.107.90)
     │
     ▼
GKE Cluster (us-central1)
     │
     ├── Pod: scorebank-api (FastAPI)
     │         └── conecta vía Cloud SQL Proxy
     │
     └── Pod: cloud-sql-proxy
               └── túnel seguro a Cloud SQL
                         └── PostgreSQL (score-bank · us-central1-a)
```

### Flujo multicloud

```
API #1 GCP          →      API #2 AWS         →      API #3 AWS
ScoreBank (tuya)           Podcasts                   Vehículos
Agrega Cliente             Agrega Podcast             Agrega Vehículo
                           GET fresco /clientes/{id}  GET fresco /clientes/{id}
```

---

## Tecnologías

| Componente | Tecnología |
|-----------|------------|
| Framework | FastAPI 0.110+ |
| Lenguaje | Python 3.13 |
| Base de datos | PostgreSQL 18 (Cloud SQL) |
| ORM | SQLAlchemy + psycopg2 |
| Validación | Pydantic v2 |
| Contenedor | Docker |
| Orquestación | Kubernetes (GKE Autopilot) |
| Registro de imágenes | Artifact Registry (GCP) |
| CI/CD | Cloud Build |
| Monitoreo | Prometheus + Grafana Cloud |
| Proxy DB | Cloud SQL Auth Proxy 2.8.0 |

---

## Estructura del proyecto

```
scoreBank/
├── app/
│   ├── models/
│   │   ├── cliente.py
│   │   ├── solicitud.py
│   │   └── evaluacion.py
│   ├── schemas/
│   │   ├── cliente.py
│   │   └── mensaje.py
│   ├── routers/
│   │   ├── cliente_router.py       # v1
│   │   ├── evaluacion_router.py    # v1
│   │   ├── solicitud_router.py     # v1
│   │   └── v2/
│   │       ├── __init__.py
│   │       └── cliente_router_v2.py # v2
│   ├── db.py
│   └── main.py
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── secret.yaml
├── Dockerfile
├── cloudbuild.yaml
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.13+
- Docker
- PostgreSQL (local o Cloud SQL)
- `gcloud` CLI
- `kubectl`

---

## Instalación local

```bash
# Clona el repositorio
git clone https://github.com/TU_USUARIO/scoreBank.git
cd scoreBank

# Crea y activa el entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instala dependencias
pip install -r requirements.txt

# Configura variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# Inicia la API
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en `http://localhost:8000/docs`.

---

## Variables de entorno

```bash
# .env
DATABASE_URL=postgresql://usuario:password@host:5432/nombre_db
API2_URL=http://podcast-api.duckdns.org
```

| Variable | Descripción |
|----------|-------------|
| `DATABASE_URL` | URL de conexión a PostgreSQL |
| `API2_URL` | URL de la API #2 (Podcasts) en AWS |

---

## Endpoints

### Base URL producción
```
http://34.41.107.90
```

### v1 — Clientes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/clientes/` | Lista todos los clientes |
| `POST` | `/clientes/` | Crea un cliente |
| `GET` | `/clientes/{id}` | Obtiene un cliente por ID |
| `PUT` | `/clientes/{id}` | Actualiza un cliente completo |
| `DELETE` | `/clientes/{id}` | Elimina un cliente |

### v2 — Clientes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v2/clientes/` | Lista todos los clientes |
| `POST` | `/api/v2/clientes/` | Crea un cliente |
| `GET` | `/api/v2/clientes/{id}` | Obtiene un cliente por ID (usado por APIs #2 y #3 para refrescar) |
| `PUT` | `/api/v2/clientes/{id}` | Reemplaza un cliente completo |
| `PATCH` | `/api/v2/clientes/{id}` | Actualización parcial de un cliente |
| `DELETE` | `/api/v2/clientes/{id}` | Elimina un cliente |
| `POST` | `/api/v2/clientes/procesar/{id}` | Inicia el flujo encadenado multicloud |

### Utilidades

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Estado de la API |
| `GET` | `/healthz` | Health check |
| `GET` | `/docs` | Documentación Swagger |
| `GET` | `/metrics` | Métricas Prometheus |

### Ejemplo de request — Crear cliente

```bash
curl -X POST http://34.41.107.90/api/v2/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Ana García",
    "ingreso_mensual": 3500000,
    "puntaje_crediticio": 720,
    "deuda_actual": 500000
  }'
```

### Ejemplo de response

```json
{
  "id": 1,
  "nombre": "Ana García",
  "ingreso_mensual": 3500000.0,
  "puntaje_crediticio": 720,
  "deuda_actual": 500000.0,
  "created_at": "2026-04-14T03:09:05"
}
```

### Validaciones

| Campo | Restricción |
|-------|------------|
| `nombre` | 2–150 caracteres |
| `ingreso_mensual` | Mayor a 0 |
| `puntaje_crediticio` | Entre 300 y 850 |
| `deuda_actual` | Mayor o igual a 0 |

---

## Flujo encadenado multicloud

El endpoint `POST /api/v2/integration/multicloud/{id}` inicia el flujo entre las tres APIs.

### Mensaje que viaja entre APIs

```json
{
  "cliente": {
    "id": 1,
    "nombre": "Ana García",
    "ingreso_mensual": 3500000.0,
    "puntaje_crediticio": 720,
    "deuda_actual": 500000.0
  },
  "podcast": null,
  "vehiculo": null
}
```

### Actualización en tiempo real

Las APIs #2 y #3 consultan `GET /api/v2/clientes/{id}` antes de reenviar o responder, garantizando que cualquier `PATCH` o `PUT` al cliente se refleje en el mensaje sin importar en qué punto de la cadena esté.

---

## Despliegue en GKE

### Requisitos previos

```bash
# Autenticación
gcloud auth login
gcloud config set project api-devops-493100

# Conectar kubectl al clúster
gcloud container clusters get-credentials scorebank-cluster --region=us-central1
```

### Crear secrets

```bash
kubectl create secret generic scorebank-secrets \
  --from-literal=DATABASE_URL="postgresql://scorebank_user:PASSWORD@127.0.0.1:5432/scorebank-db" \
  --from-literal=API2_URL="http://podcast-api.duckdns.org"

kubectl create secret generic scorebank-gcp-key \
  --from-file=key.json=scorebank-sa-key.json
```

### Desplegar

```bash
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Verificar

```bash
kubectl get pods
kubectl get service scorebank-service
```

### Construir y subir imagen manualmente

```bash
docker build -t us-central1-docker.pkg.dev/api-devops-493100/scorebank-repo/scorebank-api:VERSION .
docker push us-central1-docker.pkg.dev/api-devops-493100/scorebank-repo/scorebank-api:VERSION
kubectl rollout restart deployment scorebank-api
```

---

## CI/CD con Cloud Build

Cada push a `main` dispara automáticamente el pipeline:

```
git push origin main
       ↓
Cloud Build detecta el push
       ↓
Construye imagen Docker con tag $COMMIT_SHA
       ↓
Sube imagen al Artifact Registry
       ↓
Actualiza deployment en GKE
       ↓
API disponible en http://34.41.107.90
```

El archivo `cloudbuild.yaml` en la raíz del proyecto define los pasos del pipeline.

---

## Monitoreo

La API expone métricas en `/metrics` compatibles con Prometheus mediante `prometheus-fastapi-instrumentator`.

Las métricas incluyen número de peticiones por endpoint y método HTTP, latencia de cada endpoint (p50, p90, p99), tasa de errores 4xx y 5xx, y peticiones activas en tiempo real.

---

## Versionado

Este proyecto usa [versionado semántico](https://semver.org/) y [GitMoji](https://gitmoji.dev/) para los commits.

### Convención de commits

| Emoji | Tipo | Descripción |
|-------|------|-------------|
| ✨ | `feat` | Nueva funcionalidad |
| 🐛 | `fix` | Corrección de bug |
| 📝 | `docs` | Documentación |
| 🚀 | `deploy` | Despliegue |
| 🔧 | `config` | Configuración |
| ♻️ | `refactor` | Refactorización |
| 🐳 | `docker` | Cambios en Docker |
| ☸️ | `k8s` | Cambios en Kubernetes |

### Git Flow

```
main          ←── merge cuando está listo para producción → tag + release
  └── develop ←── integración de features
        ├── feat/nombre-feature
        └── fix/nombre-fix
```

### Releases

Los releases se generan desde tags en `main`:

```bash
git tag -a v2.0.0 -m "Release v2.0.0 - API multicloud con GKE"
git push origin main --tags
```

---

## Integrantes

| Nombre | API | Nube |
|--------|-----|------|
| Simon | API #1 — Clientes | GCP (GKE) |
| Cristian| API #2 — Podcasts | AWS |
| Jose Pablo | API #3 — Vehículos | AWS |

---

*Momento evaluativo: Abril 8 · Revisión: Abril 15 en clase*