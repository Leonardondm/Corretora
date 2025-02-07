from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth, client, category, job, report, notification, backup_routes
import threading
import time
from app.services.notification_service import check_pending_payments
from app.database import SessionLocal

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

# Inicializa o FastAPI
app = FastAPI()

# Inclui as rotas de autenticação
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Inclui as rotas de clientes
app.include_router(client.router)

# Inclui as rotas de categorias
app.include_router(category.router)

# Inclui as rotas de trabalhos
app.include_router(job.router)

# Inclui as rotas de relatórios
app.include_router(report.router)

# Inclui as rotas de notificações
app.include_router(notification.router)

app.include_router(backup_routes.router)


# Função para agendar a verificação de pagamentos
def schedule_payment_checks():
    while True:
        db = SessionLocal()
        try:
            check_pending_payments(db)
        finally:
            db.close()
        time.sleep(86400)  # Verifica a cada 24 horas (86400 segundos)

# Inicia a verificação em uma thread separada
threading.Thread(target=schedule_payment_checks, daemon=True).start()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao sistema de corretoras!"}