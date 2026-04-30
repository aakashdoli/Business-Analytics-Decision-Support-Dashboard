import streamlit as st
import plotly.express as px
import pandas as pd
from app.database.session import SessionLocal
from app.database.models import KPIResult, OperationalData
from app.ai_insights.engine import AIInsightEngine

st.set_page_config(page_title="Executive Summary", layout="wide")

def show():
    st.title("📈 Executive Summary")
    
    db = SessionLocal()
    engine = AIInsightEngine(db)
    
    # 1. AI Insights Section
    st.subheader("🤖 AI-Powered Business Insights")
    insights = engine.generate_executive_summary()
    for insight in insights:
        if "WARNING" in insight:
            st.warning(insight)
        elif "RECOMMENDATION" in insight:
            st.info(insight)
        else:
            st.write(insight)
            
    st.markdown("---")
    
    # 2. Visualizations
    col1, col2 = st.columns(2)
    
    data = db.query(OperationalData).all()
    if data:
        df = pd.DataFrame([{
            'date': d.date,
            'revenue': d.revenue,
            'costs': d.costs,
            'dept': d.department
        } for d in data])
        
        with col1:
            st.subheader("Revenue by Department")
            fig = px.pie(df, values='revenue', names='dept', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Revenue vs Costs Trend")
            df_trend = df.groupby('date').sum().reset_index()
            fig = px.line(df_trend, x='date', y=['revenue', 'costs'], 
                          labels={'value': 'Amount ($)', 'variable': 'Metric'})
            st.plotly_chart(fig, use_container_width=True)

    db.close()

if __name__ == "__main__":
    show()
