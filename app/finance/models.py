from sqlalchemy import Column, Integer, String, Numeric, DateTime
from apps.core.models import BaseModel

class FinanceTransaction(BaseModel):
    __tablename__ = 'finance_transactions'
    
    transaction_id = Column(String(100), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    processed_at = Column(DateTime)