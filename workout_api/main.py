from fastapi import FastAPI

from atletas.models import AtletaModel
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel
from routers import api_router

app = FastAPI(title="WorkoutAPI")
app.include_router(api_router)
if __name__ == "main":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
