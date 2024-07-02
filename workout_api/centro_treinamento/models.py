from sqlalchemy import Integer, String
from contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from atletas.models import AtletaModel


class CentroTreinamentoModel(BaseModel):
    __tablename__= 'centros_treinamento'
    pk_id:Mapped[int] = mapped_column(Integer, primary_key=True) 
    nome:Mapped[str] = mapped_column(String(50), unique = True, nullable=False)
    endereco:Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario:Mapped[str] = mapped_column(String(50), nullable=False)
    atleta: Mapped['AtletaModel'] = relationship(back_populates='centro_treinamento')