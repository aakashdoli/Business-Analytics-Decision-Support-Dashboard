import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.database.models import OperationalData, AnomalyLog
from app.database.session import SessionLocal
from loguru import logger

try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    logger.warning("scikit-learn not installed. Falling back to simple bounds.")

class AnomalyEngine:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def detect_anomalies(self, contamination=0.02):
        logger.info("Running Enterprise Anomaly Detection (Isolation Forest)...")
        data = self.db.query(OperationalData).all()
        if not data:
            return
        
        df = pd.DataFrame([{
            'id': d.id,
            'date': d.date,
            'region': d.region,
            'department': d.department,
            'revenue': d.revenue,
            'costs': d.costs,
            'logistics_delay': d.logistics_delay_days,
            'productivity': d.employee_productivity
        } for d in data])
        
        self.db.query(AnomalyLog).delete() # Reset anomalies for fresh analysis
        
        if HAS_SKLEARN:
            # Detect multi-dimensional anomalies per department
            for dept in df['department'].unique():
                dept_df = df[df['department'] == dept].copy()
                if len(dept_df) < 50:
                    continue
                    
                # Select features relevant to the department
                features = ['costs', 'productivity']
                if dept == 'Sales': features.append('revenue')
                if dept == 'Logistics': features.append('logistics_delay')
                
                X = dept_df[features].values
                model = IsolationForest(contamination=contamination, random_state=42)
                preds = model.fit_predict(X)
                scores = model.decision_function(X) # Lower is more anomalous
                
                dept_df['anomaly'] = preds
                dept_df['score'] = scores
                
                anomalies = dept_df[dept_df['anomaly'] == -1]
                
                for _, row in anomalies.iterrows():
                    # Determine primary cause
                    cause = "Unknown"
                    if row['productivity'] < 70: cause = "Critical productivity drop"
                    elif 'logistics_delay' in features and row['logistics_delay'] > 3: cause = "Severe logistics delay"
                    elif 'revenue' in features and row['revenue'] < dept_df['revenue'].mean() * 0.5: cause = "Revenue crash"
                    else: cause = "Unusual cost spike"
                    
                    log = AnomalyLog(
                        date=row['date'],
                        metric_name=f"{dept} Operations",
                        observed_value=float(row['costs']),
                        expected_value=float(dept_df['costs'].mean()),
                        confidence_score=float(abs(row['score']) * 100),
                        severity="Critical" if row['score'] < -0.15 else "High",
                        description=f"Incident in {row['region']} {dept}: {cause}"
                    )
                    self.db.add(log)
        else:
            # Fallback simple logic
            pass
            
        self.db.commit()
        logger.success("Anomaly detection completed.")

if __name__ == "__main__":
    engine = AnomalyEngine()
    engine.detect_anomalies()
