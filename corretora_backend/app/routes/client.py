from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.client import Client as ClientModel
from app.schemas.client import ClientCreate, Client
from typing import List

router = APIRouter(prefix="/clients", tags=["clients"])

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um novo cliente
@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = ClientModel(name=client.name, phone=client.phone, email=client.email, address=client.address)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Rota para obter todos os clientes
@router.get("/", response_model=List[Client])
def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = db.query(ClientModel).offset(skip).limit(limit).all()
    return clients

# Rota para obter um cliente específico
@router.get("/{client_id}", response_model=Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_client

# Rota para atualizar um cliente
@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for key, value in client.dict().items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

# Rota para deletar um cliente
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(db_client)
    db.commit()
    return None