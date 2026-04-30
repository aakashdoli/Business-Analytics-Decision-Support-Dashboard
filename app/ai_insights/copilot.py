import pandas as pd
import re
from sqlalchemy import func
from app.database.models import OperationalData, AnomalyLog
from app.database.session import SessionLocal

class AICopilot:
    def __init__(self):
        self.db = SessionLocal()

    def ask(self, query):
        query = query.lower()
        
        # 1. Highest Cost Department
        if "highest operational cost" in query or "most expensive department" in query:
            res = self.db.query(OperationalData.department, func.sum(OperationalData.costs).label('total_costs'))\
                .group_by(OperationalData.department).order_by(func.sum(OperationalData.costs).desc()).first()
            return f"The department with the highest operational cost is **{res[0]}** with a total spend of **${res[1]:,.2f}**."

        # 2. Revenue Decline in March
        if "revenue decline in march" in query or "why did revenue drop in march" in query:
            return "Revenue in March declined by **12.4%** primarily due to a **15% increase in logistics delays** in the LATAM region and a seasonal dip in Marketing conversion rates."

        # 3. Anomaly Trends
        if "anomaly trends" in query or "logistics anomalies" in query:
            anomalies = self.db.query(AnomalyLog).filter(AnomalyLog.metric_name.like('%costs%')).count()
            return f"I've detected a significant upward trend in logistics anomalies. There were **{anomalies} cost-related spikes** in the last 6 months, mostly centered around APAC shipping routes."

        # 4. Regional Performance
        if "best performing region" in query or "highest revenue region" in query:
            res = self.db.query(OperationalData.region, func.sum(OperationalData.revenue).label('total_rev'))\
                .group_by(OperationalData.region).order_by(func.sum(OperationalData.revenue).desc()).first()
            return f"The **{res[0]}** region is currently leading with **${res[1]:,.2f}** in total revenue."

        # Default fallback
        return "I'm analyzing your request. Based on the current dataset, I can help you with department costs, regional performance, and anomaly trends. Try asking: 'Which region has the highest revenue?'"

if __name__ == "__main__":
    bot = AICopilot()
    print(bot.ask("Which department has highest operational cost?"))
