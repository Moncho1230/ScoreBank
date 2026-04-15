import time
import logging
from fastapi import FastAPI
from app.db import Base, engine
from app.routers import cliente_router, evaluacion_router, solicitud_router
from app.routers.v2 import cliente_router_v2
from sqlalchemy import text
from prometheus_fastapi_instrumentator import Instrumentator

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ScoreBank API",
    version="2.0.0",
    description="API principal de ScoreBank",
)

Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
def startup():
    for intento in range(10):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            logger.info("Conexión a DB exitosa")
            return
        except Exception as e:
            logger.warning(f"Intento {intento + 1}/10 fallido: {e}")
            time.sleep(3)
    raise RuntimeError("No se pudo conectar a la base de datos después de 10 intentos")

# v1
app.include_router(cliente_router.router)
app.include_router(evaluacion_router.router)
app.include_router(solicitud_router.router)

# v2
app.include_router(cliente_router_v2.router, prefix="/api/v2")

@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    return {"message": "ScoreBank API activa"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)