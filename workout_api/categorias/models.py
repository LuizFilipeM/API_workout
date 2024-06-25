from sqlalchemy import Integer, String
from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relantionship

class CategoriaModel(BaseModel):
    __tablename__= 'categorias'
    pk_id:Mapped[int] = mapped_column(Integer, primary_key=True) 
    nome:Mapped[str] = mapped_column(String(50), unique = True, nullable=False)
    categoria: Mapped['AtletaModel'] = relantionship(back_populates='categoria')