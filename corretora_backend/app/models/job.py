from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    gross_value = Column(Float, nullable=False)  # Valor bruto do seguro
    broker_commission_percentage = Column(Float, nullable=False)  # % de comissão do corretor
    brokerage_commission_percentage = Column(Float, nullable=False)  # % que a corretora recebe
    net_value = Column(Float, nullable=False)  # Valor líquido a ser pago pelo cliente
    broker_commission = Column(Float, nullable=False)  # Comissão total do corretor
    brokerage_commission = Column(Float, nullable=False)  # Comissão da corretora
    broker_final_value = Column(Float, nullable=False)  # Valor final que o corretor recebe
    start_date = Column(DateTime(timezone=True), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    client = relationship("Client", back_populates="jobs")
    category = relationship("Category", back_populates="jobs")

    def __repr__(self):
        return f"<Job(id={self.id}, description={self.description})>"