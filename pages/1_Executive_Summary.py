import streamlit as st
import plotly.express as px
import pandas as pd
from app.database.session import SessionLocal
from app.database.models import KPIResult, OperationalData
from app.ai_insights.engine import AIInsightEngine
from app.utils.styles import apply_custom_styles, render_metric_card

st.set_page_config(page_title="Executive Dashboard", layout="wide")
apply_custom_styles()

def show():
    st.title("📈 Executive Performance Dashboard")
    
    db = SessionLocal()
    
    # KPI Top Bar
    kpis = db.query(KPIResult).all()
    if kpis:
        cols = st.columns(len(kpis))
        for i, kpi in enumerate(kpis):
            with cols[i]:
                render_metric_card(
                    kpi.name, 
                    f"${kpi.value:,.0f}" if "Revenue" in kpi.name else f"{kpi.value:.1f}",
                    delta=f"{kpi.mom_growth:+.1f}% MoM" if kpi.mom_growth else None
                )
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    data = db.query(OperationalData).all()
    if data:
        df = pd.DataFrame([{
            'date': d.date,
            'revenue': d.revenue,
            'costs': d.costs,
            'region': d.region,
            'dept': d.department,
            'productivity': d.employee_productivity
        } for d in data])
        
        df['date'] = pd.to_datetime(df['date'])
        
        with col1:
            st.subheader("🌍 Revenue by Region")
            fig = px.bar(df.groupby('region')['revenue'].sum().reset_index(), 
                         x='region', y='revenue', color='region',
                         template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("⚙️ Efficiency vs Costs")
            fig = px.scatter(df, x='costs', y='productivity', color='dept',
                             size='revenue', hover_name='region',
                             template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)

    db.close()

if __name__ == "__main__":
    show()
