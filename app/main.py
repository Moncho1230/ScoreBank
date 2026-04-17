import time
import logging
import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from app.db import Base, engine
from app.routers import cliente_router, evaluacion_router, solicitud_router
from app.routers.v2 import cliente_router_v2
from sqlalchemy import text
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ScoreBank API",
    version="2.0.0",
    description="API principal de ScoreBank",
)

Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
def startup():
    logger.info("API iniciada")

app.include_router(cliente_router.router, prefix="/api/v1/clientes", tags=["Clientes v1"])
app.include_router(evaluacion_router.router, prefix="/api/v1/evaluaciones", tags=["Evaluaciones v1"])
app.include_router(solicitud_router.router, prefix="/api/v1/solicitudes", tags=["Solicitudes v1"])

app.include_router(cliente_router_v2.router, prefix="/api/v2", tags=["Clientes v2"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "ScoreBank API activa"}

@app.get("/healthz", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def listar_rutas():
    for route in app.routes:
        print(route.path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)