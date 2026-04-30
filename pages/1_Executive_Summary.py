import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app.database.session import SessionLocal
from app.database.models import KPIResult, OperationalData, AnomalyLog
from app.utils.styles import apply_custom_styles, render_metric_card
import time

st.set_page_config(page_title="Executive Dashboard", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()

def show():
    st.title("📊 Executive Operational Intelligence")
    st.markdown("##### Real-time Business Analytics & Decision Support")
    
    db = SessionLocal()
    
    # 1. System Health & Live Alerts Panel
    anomalies = db.query(AnomalyLog).order_by(AnomalyLog.detected_at.desc()).limit(1).all()
    if anomalies:
        a = anomalies[0]
        st.error(f"**CRITICAL INCIDENT DETECTED:** {a.description} (Confidence: {a.confidence_score:.1f}%)")
    else:
        st.success("**SYSTEM STATUS:** All operational metrics nominal. ETL Pipeline: synced.")

    st.markdown("---")
    
    # 2. Executive KPI Cards
    kpis = db.query(KPIResult).all()
    if kpis:
        # Group KPIs logically
        cols = st.columns(len(kpis))
        for i, kpi in enumerate(kpis):
            with cols[i]:
                # Format based on metric type
                if "Revenue" in kpi.name:
                    val = f"${kpi.value/1000000:.2f}M"
                elif "%" in kpi.name or "Margin" in kpi.name or "Efficiency" in kpi.name:
                    val = f"{kpi.value:.1f}%"
                else:
                    val = f"{kpi.value:.1f}"
                    
                render_metric_card(
                    kpi.name, 
                    val,
                    delta=f"{kpi.mom_growth:+.1f}% MoM" if kpi.mom_growth else None
                )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Advanced Enterprise Charts
    data = db.query(OperationalData).all()
    if data:
        df = pd.DataFrame([{
            'date': pd.to_datetime(d.date),
            'revenue': d.revenue,
            'costs': d.costs,
            'region': d.region,
            'dept': d.department,
            'productivity': d.employee_productivity,
            'logistics': d.logistics_delay_days
        } for d in data])
        
        # Aggregate to monthly for clean executive view
        monthly_df = df.groupby(pd.Grouper(key='date', freq='ME')).agg({
            'revenue': 'sum', 'costs': 'sum', 'productivity': 'mean'
        }).reset_index()

        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Revenue vs Operational Costs (3Y Trend)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly_df['date'], y=monthly_df['revenue'], 
                                     name='Revenue', line=dict(color='#4F46E5', width=3),
                                     fill='tozeroy', fillcolor='rgba(79, 70, 229, 0.1)'))
            fig.add_trace(go.Bar(x=monthly_df['date'], y=monthly_df['costs'], 
                                 name='Ops Costs', marker_color='#EF4444', opacity=0.7))
            fig.update_layout(template='plotly_white', margin=dict(l=0, r=0, t=30, b=0),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("🌍 Regional Efficiency Distribution")
            reg_df = df.groupby('region').agg({'revenue': 'sum', 'costs': 'sum'}).reset_index()
            reg_df['margin'] = (reg_df['revenue'] - reg_df['costs']) / reg_df['revenue'] * 100
            
            fig2 = px.bar(reg_df, x='margin', y='region', orientation='h', color='region',
                          text=reg_df['margin'].apply(lambda x: f"{x:.1f}%"),
                          color_discrete_sequence=['#312E81', '#4338CA', '#4F46E5', '#6366F1'])
            fig2.update_layout(template='plotly_white', showlegend=False, 
                               xaxis_title="Operating Margin (%)", yaxis_title="")
            st.plotly_chart(fig2, use_container_width=True)

        # 4. Department Bottleneck Analysis
        st.subheader("⚙️ Departmental Bottlenecks & Productivity")
        dept_df = df.groupby('dept').agg({
            'productivity': 'mean', 'costs': 'sum', 'logistics': 'mean'
        }).reset_index()
        
        fig3 = px.scatter(dept_df, x='costs', y='productivity', size='logistics', color='dept',
                          hover_name='dept', size_max=40, template='plotly_white',
                          title="Bubble size = Logistics Delay Severity")
        fig3.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig3, use_container_width=True)

    db.close()

if __name__ == "__main__":
    show()
