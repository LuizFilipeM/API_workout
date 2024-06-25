
from typing import Annotated

from pydantic import Field
from workout_api.contrib.schemas import BaseSchema


class Atleta(BaseSchema):
    name: Annotated[str, Field(description='Nome da categoria', example = 'Scale', max_length= 10)]