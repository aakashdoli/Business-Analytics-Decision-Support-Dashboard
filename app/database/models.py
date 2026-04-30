from sqlalchemy import Column, Integer, Float, String, Date, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class OperationalData(Base):
    __tablename__ = "operations_data"
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True)
    region = Column(String, index=True)
    department = Column(String, index=True)
    revenue = Column(Float, default=0.0)
    costs = Column(Float, default=0.0)
    units_sold = Column(Integer, default=0)
    inventory_level = Column(Integer, default=0)
    logistics_delay_days = Column(Float, default=0.0)
    employee_productivity = Column(Float, default=0.0)
    headcount = Column(Integer, default=0)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class KPIResult(Base):
    __tablename__ = "kpi_results"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    period = Column(String) 
    target = Column(Float)
    trend_pct = Column(Float)
    mom_growth = Column(Float) # Month-over-Month
    yoy_growth = Column(Float) # Year-over-Year
    category = Column(String)
    health_score = Column(Float) # 0-100
    calculated_at = Column(DateTime, default=datetime.utcnow)

class AnomalyLog(Base):
    __tablename__ = "anomaly_logs"
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    metric_name = Column(String, nullable=False)
    observed_value = Column(Float)
    expected_value = Column(Float)
    confidence_score = Column(Float)
    severity = Column(String) 
    description = Column(String)
    detected_at = Column(DateTime, default=datetime.utcnow)

class ForecastResult(Base):
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True)
    metric_name = Column(String, nullable=False)
    forecast_date = Column(Date, nullable=False)
    predicted_value = Column(Float)
    lower_bound = Column(Float)
    upper_bound = Column(Float)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
