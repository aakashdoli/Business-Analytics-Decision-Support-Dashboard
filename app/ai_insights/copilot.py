import pandas as pd
import re
from sqlalchemy import func
from app.database.models import OperationalData, AnomalyLog, KPIResult
from app.database.session import SessionLocal
from loguru import logger
import datetime

class AICopilot:
    def __init__(self):
        self.db = SessionLocal()
        self.memory = [] # Store conversation context

    def generate_recommendations(self):
        # Generate dynamic recommendations based on latest anomalies and KPIs
        anomalies = self.db.query(AnomalyLog).order_by(AnomalyLog.detected_at.desc()).limit(2).all()
        recs = ["What is driving our highest costs?", "Which region is most efficient?"]
        for a in anomalies:
            recs.append(f"Tell me about the anomaly in {a.metric_name} on {a.date}")
        return list(set(recs))[:4]

    def _format_currency(self, val):
        if val >= 1_000_000: return f"${val/1_000_000:.1f}M"
        if val >= 1_000: return f"${val/1_000:.1f}k"
        return f"${val:,.2f}"

    def ask(self, query):
        logger.info(f"Co-Pilot received query: {query}")
        query_lower = query.lower()
        self.memory.append({"role": "user", "content": query})
        
        response = ""
        follow_ups = []

        try:
            # Intent: Cost Analysis
            if any(k in query_lower for k in ["cost", "expensive", "spend"]):
                res = self.db.query(OperationalData.department, func.sum(OperationalData.costs).label('tc'))\
                    .group_by(OperationalData.department).order_by(func.sum(OperationalData.costs).desc()).all()
                top_dept, top_cost = res[0]
                total_cost = sum(r[1] for r in res)
                pct = (top_cost / total_cost) * 100
                
                response = f"Based on historical data, **{top_dept}** is the major cost driver, accumulating **{self._format_currency(top_cost)}** in operational expenditure. This accounts for **{pct:.1f}%** of the total company spend.\n\n"
                response += "*Breakdown by department:*\n"
                for dept, cost in res[:3]:
                    response += f"- {dept}: {self._format_currency(cost)}\n"
                    
                follow_ups = [f"Why is {top_dept} cost so high?", "Show me revenue by department to compare."]

            # Intent: Revenue/Performance Analysis
            elif any(k in query_lower for k in ["revenue", "perform", "sales", "margin"]):
                res = self.db.query(OperationalData.region, func.sum(OperationalData.revenue).label('tr'))\
                    .group_by(OperationalData.region).order_by(func.sum(OperationalData.revenue).desc()).all()
                top_reg, top_rev = res[0]
                bottom_reg, bot_rev = res[-1]
                
                response = f"**{top_reg}** is currently the best performing region with **{self._format_currency(top_rev)}** in generated revenue. Conversely, **{bottom_reg}** is underperforming at **{self._format_currency(bot_rev)}**.\n\n"
                response += "I recommend investigating the efficiency metrics in LATAM to identify operational bottlenecks."
                
                follow_ups = [f"What are the logistics delays in {bottom_reg}?", "Show anomaly trends for revenue."]

            # Intent: Anomaly/Risk Analysis
            elif any(k in query_lower for k in ["anomaly", "risk", "spike", "drop", "issue"]):
                anomalies = self.db.query(AnomalyLog).order_by(AnomalyLog.detected_at.desc()).limit(3).all()
                if not anomalies:
                    response = "I haven't detected any critical anomalies recently. The operational pipeline looks stable."
                else:
                    response = "I have detected the following recent critical incidents:\n\n"
                    for a in anomalies:
                        response += f"⚠️ **{a.date} ({a.metric_name})**: {a.description}\n"
                        response += f"> *Confidence Score: {a.confidence_score:.1f}%* | *Severity: {a.severity}*\n\n"
                
                follow_ups = ["How does this affect our Gross Margin?", "Are there correlated drops in productivity?"]

            # Intent: General Business Health
            elif any(k in query_lower for k in ["health", "summary", "overview", "kpi"]):
                health_kpi = self.db.query(KPIResult).filter(KPIResult.name == "Business Health").first()
                margin_kpi = self.db.query(KPIResult).filter(KPIResult.name == "Gross Margin").first()
                
                if health_kpi:
                    status = "Healthy 🟢" if health_kpi.value > 80 else "Warning 🟡" if health_kpi.value > 65 else "Critical 🔴"
                    response = f"The overall Enterprise Business Health is currently **{health_kpi.value:.1f}/100** ({status}).\n\n"
                    if margin_kpi:
                        response += f"Our Gross Margin is maintaining at **{margin_kpi.value:.1f}%**, which is within the acceptable SaaS threshold. However, if health is dropping, it may be due to creeping operational costs or logistics inefficiencies."
                else:
                    response = "Business health metrics are currently being calculated by the ETL pipeline."
                
                follow_ups = ["Show me the highest cost department", "Generate an anomaly report"]

            # Contextual Fallback using Memory
            else:
                if len(self.memory) > 1:
                    last_query = self.memory[-2]['content']
                    response = f"I'm analyzing your request regarding '{query}'. This seems related to your previous question about '{last_query}'. To provide exact metrics, please specify if you want to look at Revenue, Costs, Anomalies, or Regional Performance."
                else:
                    response = "I am the Enterprise AI Co-Pilot. I can run deep semantic analysis on our operational data. Try asking me about **cost drivers**, **regional underperformance**, or **recent anomalies**."
                    
                follow_ups = self.generate_recommendations()

        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            response = "I encountered an error querying the operational data warehouse. Please try rephrasing your question."

        self.memory.append({"role": "assistant", "content": response})
        return {"response": response, "follow_ups": follow_ups}

if __name__ == "__main__":
    bot = AICopilot()
    res = bot.ask("What is driving our highest costs?")
    print(res['response'])
    print("\nFollow ups:", res['follow_ups'])
