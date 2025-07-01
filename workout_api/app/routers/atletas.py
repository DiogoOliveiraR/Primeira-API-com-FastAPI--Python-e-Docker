from fastapi import APIRouter, Depends, HTTPException, Query # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy.exc import IntegrityError # type: ignore
from fastapi_pagination import Page, paginate # type: ignore
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/atletas", tags=["Atletas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AtletaResponse)
def create_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(get_db)):
    novo = models.Atleta(**atleta.dict())
    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )

@router.get("/", response_model=Page[schemas.AtletaResponse])
def listar_atletas(nome: str = Query(None), cpf: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    return paginate(query)
