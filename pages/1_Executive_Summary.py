import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from app.database.session import SessionLocal
from app.database.models import KPIResult, OperationalData, AnomalyLog
from app.utils.styles import apply_custom_styles, render_metric_card
from app.utils.navigation import render_top_nav

st.set_page_config(page_title="Executive Dashboard", layout="wide", initial_sidebar_state="collapsed")
apply_custom_styles()
render_top_nav()

db = SessionLocal()

st.markdown("# 📊 Executive Operational Intelligence")
st.markdown('<div style="font-size:.88rem;color:#64748B;margin-bottom:1.5rem;">Real-time strategic overview · All departments · All regions</div>', unsafe_allow_html=True)

# ── System Alert Banner ────────────────────────────────────────────────────────
anomalies = db.query(AnomalyLog).order_by(AnomalyLog.detected_at.desc()).limit(1).all()
if anomalies:
    a = anomalies[0]
    st.markdown(f"""
    <div class="incident-critical" style="margin-bottom:1.5rem;">
      <div class="incident-text">🚨 <strong>ACTIVE INCIDENT:</strong> {a.description}</div>
      <div class="incident-time">Confidence {a.confidence_score:.1f}% · Severity: {a.severity} · {a.date}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="incident-success" style="margin-bottom:1.5rem;">
      <div class="incident-text">✅ <strong>ALL SYSTEMS NOMINAL</strong> — No active incidents detected across all regions.</div>
    </div>
    """, unsafe_allow_html=True)

# ── KPI Row ────────────────────────────────────────────────────────────────────
kpis = db.query(KPIResult).all()
if kpis:
    cols = st.columns(len(kpis))
    icon_map = {"Total Revenue": "💰", "Gross Margin": "📈", "Operating Margin": "📊",
                "Business Health": "💚", "Ops Efficiency": "⚡"}
    for i, kpi in enumerate(kpis):
        with cols[i]:
            val = f"${kpi.value/1_000_000:.2f}M" if "Revenue" in kpi.name else \
                  f"{kpi.value:.1f}%" if any(x in kpi.name for x in ["Margin","Efficiency"]) else \
                  f"{kpi.value:.1f}"
            delta = f"{kpi.mom_growth:+.1f}% MoM" if kpi.mom_growth else None
            render_metric_card(f"{icon_map.get(kpi.name,'📌')} {kpi.name}", val, delta)

st.markdown("<br>", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
data = db.query(OperationalData).all()
if not data:
    st.warning("No operational data found. Run the ETL pipeline from the Control Center.")
    db.close()
    st.stop()

df = pd.DataFrame([{
    'date': pd.to_datetime(d.date), 'revenue': d.revenue, 'costs': d.costs,
    'region': d.region, 'dept': d.department,
    'productivity': d.employee_productivity, 'logistics': d.logistics_delay_days
} for d in data])

monthly_df = df.groupby(pd.Grouper(key='date', freq='ME')).agg(
    {'revenue': 'sum', 'costs': 'sum', 'productivity': 'mean'}
).reset_index()

PLOTLY_DARK = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#94A3B8'),
    margin=dict(l=0, r=0, t=32, b=0),
)

# ── Revenue vs Costs Chart ─────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="section-header">📈 REVENUE VS OPERATIONAL COSTS — 3 YEAR TREND</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_df['date'], y=monthly_df['revenue'], name='Revenue',
        line=dict(color='#818CF8', width=2.5),
        fill='tozeroy', fillcolor='rgba(129,140,248,0.08)'
    ))
    fig.add_trace(go.Bar(
        x=monthly_df['date'], y=monthly_df['costs'], name='Ops Costs',
        marker_color='rgba(239,68,68,0.6)', marker_line_width=0
    ))
    fig.update_layout(**PLOTLY_DARK,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor='rgba(0,0,0,0)', borderwidth=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">🌍 REGIONAL OPERATING MARGIN</div>', unsafe_allow_html=True)
    reg_df = df.groupby('region').agg({'revenue': 'sum', 'costs': 'sum'}).reset_index()
    reg_df['margin'] = ((reg_df['revenue'] - reg_df['costs']) / reg_df['revenue'] * 100).clip(5, 55)
    fig2 = go.Figure(go.Bar(
        x=reg_df['margin'], y=reg_df['region'], orientation='h',
        marker=dict(
            color=reg_df['margin'],
            colorscale=[[0,'#EF4444'],[0.5,'#F59E0B'],[1,'#10B981']],
            showscale=False
        ),
        text=reg_df['margin'].apply(lambda x: f"{x:.1f}%"),
        textposition='inside', textfont=dict(color='white', size=11)
    ))
    fig2.update_layout(**PLOTLY_DARK, xaxis_title="Operating Margin (%)", yaxis_title="")
    st.plotly_chart(fig2, use_container_width=True)

# ── Heatmap + Correlation ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔥 OPERATIONAL HEATMAP & CORRELATION MATRIX</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    # Heatmap: avg productivity by dept × region
    pivot = df.pivot_table(values='productivity', index='dept', columns='region', aggfunc='mean')
    fig3 = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[[0,'#EF4444'],[0.5,'#F59E0B'],[1,'#10B981']],
        text=np.round(pivot.values, 1),
        texttemplate='%{text}', textfont=dict(size=11),
        showscale=True
    ))
    fig3.update_layout(**PLOTLY_DARK, title="Productivity Score by Dept × Region")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # Correlation matrix: revenue, costs, productivity, logistics
    corr_df = df[['revenue','costs','productivity','logistics']].rename(columns={
        'revenue': 'Revenue', 'costs': 'Costs', 'productivity': 'Productivity', 'logistics': 'Log. Delay'
    })
    corr = corr_df.corr()
    fig4 = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns.tolist(), y=corr.columns.tolist(),
        colorscale='RdBu', zmin=-1, zmax=1,
        text=np.round(corr.values, 2),
        texttemplate='%{text}', textfont=dict(size=12),
        showscale=True
    ))
    fig4.update_layout(**PLOTLY_DARK, title="Metric Correlation Matrix")
    st.plotly_chart(fig4, use_container_width=True)

# ── Bottleneck Bubble Chart ────────────────────────────────────────────────────
st.markdown('<div class="section-header">⚙️ DEPARTMENTAL BOTTLENECK INTELLIGENCE</div>', unsafe_allow_html=True)
dept_df = df.groupby(['dept','region']).agg(
    {'productivity': 'mean', 'costs': 'sum', 'logistics': 'mean', 'revenue': 'sum'}
).reset_index()
dept_df['efficiency'] = ((dept_df['revenue'] - dept_df['costs']) / dept_df['revenue'] * 100).clip(0, 60)

fig5 = px.scatter(
    dept_df, x='costs', y='productivity', size='logistics',
    color='dept', hover_name='dept',
    hover_data={'region': True, 'efficiency': ':.1f', 'logistics': ':.1f'},
    size_max=45,
    color_discrete_sequence=['#818CF8','#34D399','#F59E0B','#F87171','#60A5FA','#A78BFA'],
    labels={'productivity': 'Avg Productivity Score', 'costs': 'Total Operational Costs ($)'}
)
fig5.update_layout(**PLOTLY_DARK, title="Bubble = Avg Logistics Delay (days)",
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                               bgcolor='rgba(0,0,0,0)'))
st.plotly_chart(fig5, use_container_width=True)

db.close()
