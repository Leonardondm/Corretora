from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.notification import Notification as NotificationModel  # Importe o modelo SQLAlchemy
from app.schemas.notification import Notification, NotificationCreate  # Importe o schema Pydantic
from typing import List

router = APIRouter(prefix="/notifications", tags=["notifications"])

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para obter todas as notificações
@router.get("/", response_model=List[Notification])
def read_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notifications = db.query(NotificationModel).offset(skip).limit(limit).all()
    return notifications

# Rota para criar uma nova notificação
@router.post("/", response_model=Notification, status_code=201)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = NotificationModel(**notification.model_dump())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification