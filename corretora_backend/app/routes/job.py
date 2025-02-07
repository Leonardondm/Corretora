from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.job import Job as JobModel
from app.schemas.job import JobCreate, Job
from typing import List

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um novo trabalho
@router.post("/", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    # Cálculos automáticos
    broker_commission = (job.gross_value * job.broker_commission_percentage) / 100
    brokerage_commission = (broker_commission * job.brokerage_commission_percentage) / 100
    broker_final_value = broker_commission - brokerage_commission
    net_value = job.gross_value - broker_commission

    # Cria o modelo Job com os valores calculados
    db_job = JobModel(
        description=job.description,
        gross_value=job.gross_value,
        broker_commission_percentage=job.broker_commission_percentage,
        brokerage_commission_percentage=job.brokerage_commission_percentage,
        net_value=net_value,
        broker_commission=broker_commission,
        brokerage_commission=brokerage_commission,
        broker_final_value=broker_final_value,
        start_date=job.start_date,
        payment_date=job.payment_date,
        client_id=job.client_id,
        category_id=job.category_id,
        notes=job.notes
    )

    # Adiciona o trabalho ao banco de dados
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# Rota para obter todos os trabalhos
@router.get("/", response_model=List[Job])
def read_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = db.query(JobModel).offset(skip).limit(limit).all()
    return jobs

# Rota para obter um trabalho específico
@router.get("/{job_id}", response_model=Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Trabalho não encontrado")
    return db_job

# Rota para atualizar um trabalho
@router.put("/{job_id}", response_model=Job)
def update_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Trabalho não encontrado")
    for key, value in job.dict().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

# Rota para deletar um trabalho
@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Trabalho não encontrado")
    db.delete(db_job)
    db.commit()
    return None