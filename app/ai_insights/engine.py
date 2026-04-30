import pandas as pd
from sqlalchemy.orm import Session
from app.database.models import OperationalData, KPIResult, AnomalyLog
from app.database.session import SessionLocal

class AIInsightEngine:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def generate_executive_summary(self):
        kpis = self.db.query(KPIResult).all()
        anomalies = self.db.query(AnomalyLog).order_by(AnomalyLog.detected_at.desc()).limit(5).all()
        
        insights = []
        
        # 1. Financial Health
        rev = next((k for k in kpis if k.name == "Total Revenue"), None)
        margin = next((k for k in kpis if k.name == "Gross Margin %"), None)
        
        if rev:
            insights.append(f"Total revenue stands at ${rev.value:,.2f}.")
        if margin and margin.value < 20:
            insights.append("WARNING: Gross margin is below the 20% threshold, suggesting rising operational costs.")
        elif margin:
            insights.append(f"Gross margin is healthy at {margin.value:.1f}%.")
            
        # 2. Anomalies
        if anomalies:
            insights.append(f"System detected {len(anomalies)} recent anomalies that require immediate attention.")
            for a in anomalies:
                insights.append(f"- Alert: {a.description} on {a.date} (Metric: {a.metric_name})")
                
        # 3. Recommendations
        efficiency = next((k for k in kpis if k.name == "Ops Efficiency"), None)
        if efficiency and efficiency.value < 5:
            insights.append("RECOMMENDATION: Review manufacturing workflows to improve units produced per headcount.")
            
        return insights

if __name__ == "__main__":
    engine = AIInsightEngine()
    print("\n".join(engine.generate_executive_summary()))
