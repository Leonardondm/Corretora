from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.notification import Notification
from app.database import SessionLocal

def check_pending_payments(db: Session):
    # Obtém a data atual
    today = datetime.now()

    # Verifica trabalhos com pagamentos atrasados
    overdue_jobs = db.query(Job).filter(
        Job.payment_date < today
    ).all()

    # Verifica trabalhos com pagamentos próximos do vencimento (7 dias antes)
    upcoming_jobs = db.query(Job).filter(
        Job.payment_date >= today,
        Job.payment_date <= today + timedelta(days=7)
    ).all()

    # Cria notificações para trabalhos atrasados
    for job in overdue_jobs:
        message = f"Pagamento atrasado para o trabalho: {job.description}"
        db_notification = Notification(message=message, job_id=job.id)
        db.add(db_notification)

    # Cria notificações para trabalhos próximos do vencimento
    for job in upcoming_jobs:
        message = f"Pagamento próximo do vencimento para o trabalho: {job.description}"
        db_notification = Notification(message=message, job_id=job.id)
        db.add(db_notification)

    # Salva as notificações no banco de dados
    db.commit()