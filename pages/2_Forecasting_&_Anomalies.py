import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.database.session import SessionLocal
from app.database.models import ForecastResult, AnomalyLog, OperationalData
from app.utils.styles import apply_custom_styles
from app.utils.navigation import render_top_nav

st.set_page_config(page_title="Forecast & Anomaly Intelligence", layout="wide", initial_sidebar_state="collapsed")
apply_custom_styles()
render_top_nav()

db = SessionLocal()

st.markdown("# 🔮 Predictive Analytics & Incident Intelligence")
st.markdown('<div style="font-size:.88rem;color:#64748B;margin-bottom:1.5rem;">Prophet ML forecasting · Isolation Forest anomaly detection · 95% confidence intervals</div>', unsafe_allow_html=True)

PLOTLY_DARK = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#94A3B8'),
    margin=dict(l=0, r=0, t=32, b=0),
)

tab1, tab2 = st.tabs(["📈 Multi-Metric Forecast", "🚨 Incident Logs"])

with tab1:
    metrics = ["Total Revenue", "Total Costs", "Efficiency Score"]
    selected_metric = st.selectbox("Select Metric", metrics, key="fc_metric")

    # Historical data
    hist_data = db.query(OperationalData).all()
    df_hist = pd.DataFrame([{
        'date': pd.to_datetime(d.date),
        'Total Revenue': d.revenue,
        'Total Costs': d.costs,
        'Efficiency Score': d.employee_productivity
    } for d in hist_data])

    if selected_metric == 'Efficiency Score':
        df_hist = df_hist.groupby('date').mean().reset_index()
    else:
        df_hist = df_hist.groupby('date').sum().reset_index()

    forecasts = db.query(ForecastResult).filter(
        ForecastResult.metric_name == selected_metric
    ).order_by(ForecastResult.forecast_date).all()

    if forecasts:
        f_df = pd.DataFrame([{
            'date': pd.to_datetime(f.forecast_date),
            'predicted': f.predicted_value,
            'lower': f.lower_bound,
            'upper': f.upper_bound,
            'model': f.model_version
        } for f in forecasts])

        model_label = f_df['model'].iloc[0] if len(f_df) else "ML Model"

        # Anomaly overlay dates
        all_anomalies = db.query(AnomalyLog).all()

        # Last 90 days of history
        cutoff = f_df['date'].min() - pd.Timedelta(days=90)
        df_recent = df_hist[df_hist['date'] >= cutoff]

        fig = go.Figure()

        # Historical
        fig.add_trace(go.Scatter(
            x=df_recent['date'], y=df_recent[selected_metric],
            name='Historical', mode='lines',
            line=dict(color='#475569', width=1.5)
        ))

        # Confidence band
        if f_df['upper'].notnull().any():
            fig.add_trace(go.Scatter(
                x=f_df['date'], y=f_df['upper'],
                mode='lines', line_color='rgba(0,0,0,0)', showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=f_df['date'], y=f_df['lower'],
                fill='tonexty', mode='lines',
                fillcolor='rgba(129,140,248,0.15)',
                line_color='rgba(0,0,0,0)',
                name='95% Confidence Band'
            ))

        # Forecast line
        fig.add_trace(go.Scatter(
            x=f_df['date'], y=f_df['predicted'],
            name=f'Forecast ({model_label})',
            line=dict(color='#818CF8', width=2.5, dash='dot')
        ))

        # Anomaly markers
        anomaly_dates = set(pd.to_datetime(a.date) for a in all_anomalies)
        anom_mask = df_recent['date'].isin(anomaly_dates)
        if anom_mask.any():
            fig.add_trace(go.Scatter(
                x=df_recent.loc[anom_mask, 'date'],
                y=df_recent.loc[anom_mask, selected_metric],
                mode='markers', name='Detected Incident',
                marker=dict(color='#EF4444', size=9, symbol='x-thin',
                            line=dict(color='#EF4444', width=2),
                            opacity=0.85)
            ))

        fig.update_layout(
            **PLOTLY_DARK,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig, use_container_width=True)

        # Mini stats
        c1, c2, c3 = st.columns(3)
        c1.metric("30-Day Forecast Avg", f"{f_df['predicted'].mean():,.0f}")
        c2.metric("Forecast Upper Bound", f"{f_df['upper'].mean():,.0f}" if f_df['upper'].notnull().any() else "N/A")
        c3.metric("Model", model_label.split()[0])

    else:
        st.info("No forecast data available. Run the forecasting engine from the Control Center.")

with tab2:
    st.markdown('<div class="section-header">🚨 INCIDENT LOG — ISOLATION FOREST DETECTIONS</div>', unsafe_allow_html=True)

    anomalies = db.query(AnomalyLog).order_by(AnomalyLog.date.desc()).all()

    if anomalies:
        # Summary counters
        critical = sum(1 for a in anomalies if a.severity == "Critical")
        high_sev = sum(1 for a in anomalies if a.severity == "High")

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Incidents Detected", len(anomalies))
        m2.metric("Critical", critical, delta="Requires action", delta_color="inverse")
        m3.metric("High Severity", high_sev)

        st.markdown("<br>", unsafe_allow_html=True)

        a_df = pd.DataFrame([{
            'Date': str(a.date),
            'Dept / Metric': a.metric_name,
            'Observed': f"{a.observed_value:,.1f}",
            'Expected': f"{a.expected_value:,.1f}",
            'Confidence': f"{a.confidence_score:.1f}%",
            'Severity': a.severity,
            'Description': a.description
        } for a in anomalies])

        def highlight_severity(val):
            if val == 'Critical':
                return 'color: #EF4444; font-weight: 700'
            elif val == 'High':
                return 'color: #F59E0B; font-weight: 600'
            return ''

        st.dataframe(
            a_df.style.map(highlight_severity, subset=['Severity']),
            use_container_width=True,
            height=450
        )

        # Severity distribution chart
        sev_counts = a_df['Severity'].value_counts().reset_index()
        sev_counts.columns = ['Severity', 'Count']
        fig_sev = px.bar(sev_counts, x='Severity', y='Count', color='Severity',
                         color_discrete_map={'Critical': '#EF4444', 'High': '#F59E0B'},
                         template='plotly_dark')
        fig_sev.update_layout(**PLOTLY_DARK, title="Incident Severity Distribution")
        st.plotly_chart(fig_sev, use_container_width=True)
    else:
        st.success("No anomalies detected in the current period. All systems nominal.")

db.close()
