import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy.orm import Session
from app.database.models import OperationalData, AnomalyLog
from app.database.session import SessionLocal
from loguru import logger

class AnomalyEngine:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def detect_anomalies(self, threshold=3):
        data = self.db.query(OperationalData).all()
        if not data:
            return
        
        df = pd.DataFrame([{
            'id': d.id,
            'date': d.date,
            'revenue': d.revenue,
            'costs': d.costs
        } for d in data])
        
        metrics = ['revenue', 'costs']
        
        for metric in metrics:
            # Calculate Z-score
            z_scores = np.abs(stats.zscore(df[metric]))
            anomalies = df[z_scores > threshold]
            
            for _, row in anomalies.iterrows():
                # Check if already logged to avoid duplicates
                exists = self.db.query(AnomalyLog).filter(
                    AnomalyLog.date == row['date'],
                    AnomalyLog.metric_name == metric
                ).first()
                
                if not exists:
                    log = AnomalyLog(
                        date=row['date'],
                        metric_name=metric,
                        observed_value=row[metric],
                        expected_value=df[metric].mean(),
                        confidence_score=float(z_scores[row.name]),
                        severity="High" if z_scores[row.name] > 5 else "Medium",
                        description=f"Significant {metric} deviation detected."
                    )
                    self.db.add(log)
                    
        self.db.commit()
        logger.success("Anomaly detection completed.")

if __name__ == "__main__":
    engine = AnomalyEngine()
    engine.detect_anomalies()
