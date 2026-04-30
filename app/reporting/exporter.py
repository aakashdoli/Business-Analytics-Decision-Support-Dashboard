import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import KPIResult, AnomalyLog
from app.database.session import SessionLocal
import os

def generate_executive_report():
    db = SessionLocal()
    
    report = []
    report.append("# Enterprise Operational Intelligence Report")
    report.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("---\n")
    
    # KPIs Section
    report.append("## 1. Executive Key Performance Indicators\n")
    kpis = db.query(KPIResult).all()
    for kpi in kpis:
        val = f"${kpi.value:,.2f}" if "Revenue" in kpi.name else f"{kpi.value:.2f}%" if "Margin" in kpi.name or "Efficiency" in kpi.name else f"{kpi.value:.1f}"
        growth = f" ({kpi.mom_growth:+.1f}% MoM)" if kpi.mom_growth else ""
        report.append(f"- **{kpi.name}**: {val}{growth}")
        
    report.append("\n---\n")
    
    # Anomalies Section
    report.append("## 2. Recent Critical Incidents (Isolation Forest)\n")
    anomalies = db.query(AnomalyLog).order_by(AnomalyLog.detected_at.desc()).limit(5).all()
    if not anomalies:
        report.append("*No critical incidents detected in the current period.*")
    else:
        for a in anomalies:
            icon = "🔴" if a.severity == "Critical" else "🟡"
            report.append(f"### {icon} [{a.date}] {a.severity} Incident: {a.metric_name}")
            report.append(f"> {a.description}")
            report.append(f"> **Confidence Score:** {a.confidence_score:.1f}%\n")
            
    # Save
    os.makedirs('reports', exist_ok=True)
    filename = f"reports/Executive_Summary_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(filename, 'w') as f:
        f.write("\n".join(report))
        
    db.close()
    return filename

if __name__ == "__main__":
    filepath = generate_executive_report()
    print(f"Report generated at: {filepath}")
