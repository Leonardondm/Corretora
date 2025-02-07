from pydantic import BaseModel
from datetime import datetime
from typing import List

class ReportPeriod(BaseModel):
    start_date: datetime
    end_date: datetime

class TotalReceivedResponse(BaseModel):
    total_received: float

class TotalToReceiveResponse(BaseModel):
    total_to_receive: float

class JobDetail(BaseModel):
    id: int
    description: str
    client_name: str
    category_name: str
    gross_value: float  # Valor bruto do seguro
    broker_commission: float  # Comissão do corretor
    brokerage_commission: float  # Comissão da corretora
    net_value: float  # Valor líquido a ser pago pelo cliente
    broker_final_value: float  # Valor final que o corretor recebe
    start_date: datetime
    payment_date: datetime

class DetailedReportResponse(BaseModel):
    jobs: List[JobDetail]
    total_net_value: float
    total_broker_commission: float
    total_brokerage_commission: float
    total_broker_final_value: float

class ReportPeriod(BaseModel):
    start_date: datetime
    end_date: datetime