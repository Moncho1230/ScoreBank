from fastapi import FastAPI
from app.db import Base, engine

app = FastAPI(
	title="ScoreBank API",
	version="1.0.0",
	description="API principal de ScoreBank",
)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
	return {"message": "ScoreBank API activa"}


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
	return {"status": "ok"}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
