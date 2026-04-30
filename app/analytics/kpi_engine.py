import pandas as pd
from sqlalchemy.orm import Session
from app.database.models import OperationalData, KPIResult
from app.database.session import SessionLocal
from loguru import logger

class KPIEngine:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def calculate_all_kpis(self):
        logger.info("Starting advanced KPI calculations...")
        data = self.db.query(OperationalData).all()
        if not data:
            return
        
        df = pd.DataFrame([{
            'date': pd.to_datetime(d.date),
            'revenue': d.revenue,
            'costs': d.costs,
            'productivity': d.employee_productivity
        } for d in data])
        
        # Monthly aggregation for growth metrics
        monthly = df.set_index('date').resample('ME').sum()
        
        # 1. Total Revenue & Growth
        latest_rev = monthly['revenue'].iloc[-1]
        prev_rev = monthly['revenue'].iloc[-2] if len(monthly) > 1 else latest_rev
        mom_growth = ((latest_rev - prev_rev) / prev_rev * 100) if prev_rev > 0 else 0
        
        yoy_rev = monthly['revenue'].iloc[-13] if len(monthly) > 12 else None
        yoy_growth = ((latest_rev - yoy_rev) / yoy_rev * 100) if yoy_rev and yoy_rev > 0 else 0
        
        # 2. Health Score (Efficiency + Productivity)
        avg_productivity = df['productivity'].mean()
        margin = ((df['revenue'].sum() - df['costs'].sum()) / df['revenue'].sum() * 100)
        health_score = (avg_productivity * 0.4) + (margin * 0.6)
        health_score = max(0, min(100, health_score)) # Clamp 0-100

        self.db.query(KPIResult).delete() # Reset
        
        self._save_kpi("Total Revenue", latest_rev, "Latest Month", 
                       mom_growth=mom_growth, yoy_growth=yoy_growth, category="Financial")
        
        self._save_kpi("Business Health", health_score, "Current", 
                       category="Strategic", health_score=health_score)
        
        self._save_kpi("Gross Margin %", margin, "All Time", category="Financial")
        
        self.db.commit()
        logger.success("KPI calculations completed.")

    def _save_kpi(self, name, value, period, mom_growth=0, yoy_growth=0, category="General", health_score=None):
        kpi = KPIResult(
            name=name,
            value=float(value),
            period=period,
            mom_growth=float(mom_growth),
            yoy_growth=float(yoy_growth),
            category=category,
            health_score=float(health_score) if health_score is not None else None
        )
        self.db.add(kpi)

if __name__ == "__main__":
    engine = KPIEngine()
    engine.calculate_all_kpis()
