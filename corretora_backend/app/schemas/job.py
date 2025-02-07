from pydantic import BaseModel
from datetime import datetime

class JobBase(BaseModel):
    description: str
    gross_value: float
    broker_commission_percentage: float  # % de comissão do corretor
    brokerage_commission_percentage: float  # % que a corretora recebe
    start_date: datetime
    payment_date: datetime
    client_id: int
    category_id: int
    notes: str | None = None

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    net_value: float  # Valor líquido a ser pago pelo cliente
    broker_commission: float  # Comissão total do corretor
    brokerage_commission: float  # Comissão da corretora
    broker_final_value: float  # Valor final que o corretor recebe
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True