from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.database import SessionLocal
from app.models.job import Job
from app.schemas.report import ReportPeriod, TotalReceivedResponse, TotalToReceiveResponse, JobDetail, DetailedReportResponse
from datetime import datetime, timedelta

router = APIRouter(prefix="/reports", tags=["reports"])

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para obter o total recebido em um período
@router.post("/total-received", response_model=TotalReceivedResponse)
def get_total_received(period: ReportPeriod, db: Session = Depends(get_db)):
    total_received = db.query(func.sum(Job.broker_final_value)).filter(
        Job.payment_date >= period.start_date,
        Job.payment_date <= period.end_date
    ).scalar()
    return {"total_received": total_received or 0.0}

# Rota para obter o total a receber no próximo mês
@router.get("/total-to-receive", response_model=TotalToReceiveResponse)
def get_total_to_receive(db: Session = Depends(get_db)):
    # Obtém a data atual
    today = datetime.now()

    # Calcula o início do próximo mês
    next_month_start = (today.replace(day=1) + timedelta(days=32)).replace(day=1)

    # Calcula o fim do próximo mês
    next_month_end = (next_month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Filtra os trabalhos com payment_date dentro do próximo mês
    total_to_receive = db.query(func.sum(Job.broker_final_value)).filter(
        Job.payment_date >= next_month_start,
        Job.payment_date <= next_month_end
    ).scalar()

    return {"total_to_receive": total_to_receive or 0.0}

# Rota para obter um relatório detalhado
@router.get("/detailed-report", response_model=DetailedReportResponse)
def get_detailed_report(db: Session = Depends(get_db)):
    # Consulta os trabalhos com detalhes do cliente e da categoria
    jobs = db.query(Job).options(
        joinedload(Job.client),
        joinedload(Job.category)
    ).all()

    # Calcula os totais
    total_net_value = sum(job.net_value for job in jobs)
    total_broker_commission = sum(job.broker_commission for job in jobs)
    total_brokerage_commission = sum(job.brokerage_commission for job in jobs)
    total_broker_final_value = sum(job.broker_final_value for job in jobs)

    # Formata os detalhes dos trabalhos
    job_details = [
        JobDetail(
            id=job.id,
            description=job.description,
            client_name=job.client.name,
            category_name=job.category.name,
            gross_value=job.gross_value,
            broker_commission=job.broker_commission,
            brokerage_commission=job.brokerage_commission,
            net_value=job.net_value,
            broker_final_value=job.broker_final_value,
            start_date=job.start_date,
            payment_date=job.payment_date
        )
        for job in jobs
    ]

    return {
        "jobs": job_details,
        "total_net_value": total_net_value,
        "total_broker_commission": total_broker_commission,
        "total_brokerage_commission": total_brokerage_commission,
        "total_broker_final_value": total_broker_final_value
    }



from fastapi.responses import StreamingResponse
import io
import openpyxl


# Rota para exportar relatórios em Excel
@router.get("/export-detailed-report-excel")
def export_detailed_report_excel(db: Session = Depends(get_db)):
    # Consulta os trabalhos com detalhes do cliente e da categoria
    jobs = db.query(Job).options(
        joinedload(Job.client),
        joinedload(Job.category)
    ).all()

    # Cria um arquivo Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Relatório Detalhado"

    # Adiciona cabeçalhos
    sheet.append([
        "ID", "Descrição", "Cliente", "Categoria", "Valor Bruto", "Comissão do Corretor",
        "Comissão da Corretora", "Valor Líquido", "Valor Final do Corretor", "Data de Início", "Data de Pagamento"
    ])

    # Adiciona dados
    for job in jobs:
        # Remove o fuso horário das datas
        start_date_naive = job.start_date.replace(tzinfo=None)
        payment_date_naive = job.payment_date.replace(tzinfo=None)

        sheet.append([
            job.id,
            job.description,
            job.client.name,
            job.category.name,
            job.gross_value,
            job.broker_commission,
            job.brokerage_commission,
            job.net_value,
            job.broker_final_value,
            start_date_naive,
            payment_date_naive
        ])

    # Adiciona os totais
    total_net_value = sum(job.net_value for job in jobs)
    total_broker_commission = sum(job.broker_commission for job in jobs)
    total_brokerage_commission = sum(job.brokerage_commission for job in jobs)
    total_broker_final_value = sum(job.broker_final_value for job in jobs)

    sheet.append([])
    sheet.append(["Total Líquido", "", "", "", "", "", "", total_net_value])
    sheet.append(["Total Comissão do Corretor", "", "", "", "", "", "", total_broker_commission])
    sheet.append(["Total Comissão da Corretora", "", "", "", "", "", "", total_brokerage_commission])
    sheet.append(["Total Valor Final do Corretor", "", "", "", "", "", "", total_broker_final_value])

    # Salva o arquivo em memória
    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Retorna o arquivo como resposta
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=relatorio_detalhado.xlsx"}
    )