from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from atletas.models import AtletaModel
from atletas.schemas import AtletaIn, AtletaOut, AtletaReturn, AtletaUpdate
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel
from configs import database
from contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DatabaseDependency, atletas_in: AtletaIn = Body(...)):
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=atletas_in.categoria.nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria nao encontrada"
        )

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(
                    nome=atletas_in.centro_treinamento.nome
                )
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="centro treinamento nao encontrado",
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.utcnow(), **atletas_in.model_dump()
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError as e:
        if "UniqueViolationError" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER, detail="CPF ou Nome já existe."
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco",
        )

    return atleta_out


@router.get(
    "/",
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaReturn],
)
async def query(db_session: DatabaseDependency) -> list[AtletaReturn]:
    atletas: list[AtletaReturn] = (
        (await db_session.execute(select(AtletaModel))).scalars().all()
    )
    resultado = [AtletaReturn.model_validate(atleta) for atleta in atletas]

    return resultado


@router.get(
    "/{id}",
    summary="Consultar atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="atleta nao encontrado"
        )

    return atleta


@router.patch(
    "/{id}",
    summary="editar atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(
    id: UUID4, db_session: DatabaseDependency, atletas_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria nao encontrada"
        )

    atleta_update = atletas_up.model_dump(exclude_unset=True)

    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    "/{id}", summary="deletar atleta pelo id", status_code=status.HTTP_204_NO_CONTENT
)
async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="atleta nao encontrado"
        )

    await db_session.delete(atleta)
    await db_session.commit()


def get_db():
    db = database.get_session()
    yield db


@router.get("/items/", response_model=list[AtletaOut])
async def read_items(
    nome: Optional[str] = Query(None, description="Filter by name"),
    idade: Optional[int] = Query(None, description="Filter by idade"),
    db: AsyncSession = Depends(database.get_session),
):
    query = select(AtletaModel)

    # Filtros básicos
    if nome:
        query = query.filter(AtletaModel.nome == nome)
    if idade:
        query = query.filter(AtletaModel.idade == idade)

    result = await db.execute(
        query.options(
            selectinload(AtletaModel.categoria),
            selectinload(AtletaModel.centro_treinamento),
        )
    )
    items = result.scalars().all()

    if not items:
        raise HTTPException(status_code=404, detail="No items found")

    return items


add_pagination(router)
