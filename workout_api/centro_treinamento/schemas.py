
from typing import Annotated

from pydantic import Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    name: Annotated[str, Field(description='Nome do centro de treinamento', example = 'CT king', max_length= 20)]
    endereco: Annotated[str, Field(description='Nome do proprietario', example = 'Joao', max_length= 50)]
    proprietario: Annotated[str, Field(description='endereco do centro de treinamento', example = 'Rua 1, nmr 2', max_length= 60)]