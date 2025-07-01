from sqlalchemy import Column, Integer, String # type: ignore
from app.database import Base

class Atleta(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cpf = Column(String, unique=True, index=True, nullable=False)
    centro_treinamento = Column(String)
    categoria = Column(String)
