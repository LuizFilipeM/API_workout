from typing import Annotated

from pydantic import UUID4, Field

from contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT king",
            max_length=20,
        ),
    ]
    proprietario: Annotated[
        str, Field(description="Nome do proprietario", example="Joao", max_length=50)
    ]
    endereco: Annotated[
        str,
        Field(
            description="endereco do centro de treinamento",
            example="Rua 1, nmr 2",
            max_length=60,
        ),
    ]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT king",
            max_length=20,
        ),
    ]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="Identificador do centro de treinamento")]
