from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class AppLog(BaseModel):
    __tablename__ = 'app_logs'
    
    app_name = Column(String(50), nullable=False)
    dag_id = Column(String(250), nullable=False)
    task_id = Column(String(250), nullable=False)
    log_level = Column(String(10), nullable=False)
    message = Column(Text)