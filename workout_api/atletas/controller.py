from fastapi import APIRouter, Body, status
from contrib.dependencies import DatabaseDependency
from atletas.schemas import AtletaIn


router = APIRouter()

@router.post('/',
             summary = 'Criar novo atleta',
             status_code=status.HTTP_201_CREATED)

async def post(db_session: DatabaseDependency,
               atletas_in:AtletaIn = Body(...)
               ):
    pass