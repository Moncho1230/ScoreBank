from fastapi import FastAPI
from app.db import Base, engine
from app.routers import cliente_router, evaluacion_router, solicitud_router

app = FastAPI(
	title="ScoreBank API",
	version="1.0.0",
	description="API principal de ScoreBank",
)

Base.metadata.create_all(bind=engine)

app.include_router(cliente_router.router)
app.include_router(evaluacion_router.router)
app.include_router(solicitud_router.router)



@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
	return {"message": "ScoreBank API activa"}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
