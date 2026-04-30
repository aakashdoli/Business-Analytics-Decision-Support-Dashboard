import pandas as pd
from sqlalchemy.orm import Session
from app.database.models import OperationalData, KPIResult
from app.database.session import SessionLocal

class KPIEngine:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def calculate_all_kpis(self):
        # Fetch all operational data
        data = self.db.query(OperationalData).all()
        if not data:
            return
        
        df = pd.DataFrame([{
            'date': d.date,
            'department': d.department,
            'revenue': d.revenue,
            'costs': d.costs,
            'units_produced': d.units_produced,
            'units_sold': d.units_sold,
            'headcount': d.headcount
        } for d in data])
        
        df['date'] = pd.to_datetime(df['date'])
        
        # 1. Total Revenue
        total_revenue = df['revenue'].sum()
        self._save_kpi("Total Revenue", total_revenue, "All Time", category="Financial")
        
        # 2. Gross Margin
        total_costs = df['costs'].sum()
        gross_margin = ((total_revenue - total_costs) / total_revenue * 100) if total_revenue > 0 else 0
        self._save_kpi("Gross Margin %", gross_margin, "All Time", category="Financial")
        
        # 3. Operational Efficiency (Units Produced / Headcount)
        total_produced = df['units_produced'].sum()
        total_headcount = df['headcount'].sum()
        efficiency = (total_produced / total_headcount) if total_headcount > 0 else 0
        self._save_kpi("Ops Efficiency", efficiency, "All Time", category="Operations")
        
        # 4. Sales Conversion Rate
        total_sold = df['units_sold'].sum()
        conversion = (total_sold / total_produced * 100) if total_produced > 0 else 0
        self._save_kpi("Sales Conversion %", conversion, "All Time", category="Sales")

        self.db.commit()

    def _save_kpi(self, name, value, period, target=None, category="General"):
        kpi = KPIResult(
            name=name,
            value=float(value),
            period=period,
            target=target,
            category=category
        )
        self.db.add(kpi)

if __name__ == "__main__":
    engine = KPIEngine()
    engine.calculate_all_kpis()
