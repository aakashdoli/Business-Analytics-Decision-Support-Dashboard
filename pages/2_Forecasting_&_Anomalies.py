import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app.database.session import SessionLocal
from app.database.models import ForecastResult, AnomalyLog, OperationalData
from app.utils.styles import apply_custom_styles

st.set_page_config(page_title="Forecasting & Anomalies", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()

def show():
    st.title("🔮 Predictive Analytics & Anomalies")
    st.markdown("##### ML-powered Forecasting & Isolation Forest Incident Detection")
    st.markdown("---")
    
    db = SessionLocal()
    
    tab1, tab2 = st.tabs(["Multi-Metric Forecast (Prophet)", "Incident Logs"])
    
    with tab1:
        metrics = ["Total Revenue", "Total Costs", "Efficiency Score"]
        selected_metric = st.selectbox("Select Metric to Forecast", metrics)
        
        # Get historical data
        hist_data = db.query(OperationalData).all()
        if hist_data:
            df_hist = pd.DataFrame([{
                'date': pd.to_datetime(d.date),
                'Total Revenue': d.revenue,
                'Total Costs': d.costs,
                'Efficiency Score': d.employee_productivity
            } for d in hist_data])
            df_hist = df_hist.groupby('date').sum().reset_index() if selected_metric != 'Efficiency Score' else df_hist.groupby('date').mean().reset_index()
        
        # Get forecast data
        forecasts = db.query(ForecastResult).filter(ForecastResult.metric_name == selected_metric).order_by(ForecastResult.forecast_date).all()
        
        if forecasts and not df_hist.empty:
            f_df = pd.DataFrame([{
                'date': pd.to_datetime(f.forecast_date),
                'predicted': f.predicted_value,
                'lower': f.lower_bound,
                'upper': f.upper_bound
            } for f in forecasts])
            
            # Get anomalies for overlay
            anomalies = db.query(AnomalyLog).all()
            anomaly_dates = [pd.to_datetime(a.date) for a in anomalies if selected_metric.split(' ')[1].lower() in a.metric_name.lower() or 'Operations' in a.metric_name]
            
            fig = go.Figure()
            
            # Historical
            # Only show last 90 days of history for clarity
            df_hist_recent = df_hist[df_hist['date'] >= (f_df['date'].min() - pd.Timedelta(days=90))]
            fig.add_trace(go.Scatter(x=df_hist_recent['date'], y=df_hist_recent[selected_metric], 
                                     mode='lines', name='Historical Data', line=dict(color='#94A3B8')))
            
            # Forecast
            fig.add_trace(go.Scatter(x=f_df['date'], y=f_df['predicted'], 
                                     mode='lines', name='Forecast', line=dict(color='#4F46E5', dash='dot', width=3)))
            
            # Confidence Band
            if f_df['upper'].notnull().any():
                fig.add_trace(go.Scatter(x=f_df['date'], y=f_df['upper'], mode='lines', line_color='rgba(0,0,0,0)', showlegend=False))
                fig.add_trace(go.Scatter(x=f_df['date'], y=f_df['lower'], fill='tonexty', mode='lines', 
                                         fillcolor='rgba(79, 70, 229, 0.2)', line_color='rgba(0,0,0,0)', name='95% Confidence Interval'))
            
            # Anomaly Overlay
            if anomaly_dates:
                overlay_y = df_hist_recent[df_hist_recent['date'].isin(anomaly_dates)][selected_metric]
                overlay_x = df_hist_recent[df_hist_recent['date'].isin(anomaly_dates)]['date']
                fig.add_trace(go.Scatter(x=overlay_x, y=overlay_y, mode='markers', 
                                         marker=dict(color='#EF4444', size=10, symbol='x'), name='Detected Incident'))

            fig.update_layout(template='plotly_white', hovermode='x unified', 
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No forecast data available. Run the forecasting engine from the Data Center.")

    with tab2:
        st.subheader("Detected System Incidents (Isolation Forest)")
        anomalies = db.query(AnomalyLog).order_by(AnomalyLog.date.desc()).all()
        
        if anomalies:
            a_df = pd.DataFrame([{
                'Date': a.date,
                'Department/Metric': a.metric_name,
                'Observed Value': f"{a.observed_value:,.2f}",
                'Confidence': f"{a.confidence_score:.1f}%",
                'Severity': a.severity,
                'Incident Details': a.description
            } for a in anomalies])
            
            def color_severity(val):
                color = '#EF4444' if val == 'Critical' else '#F59E0B'
                return f'color: {color}; font-weight: bold'
                
            st.dataframe(a_df.style.map(color_severity, subset=['Severity']), use_container_width=True)
        else:
            st.success("No anomalies detected in the current period.")

    db.close()

if __name__ == "__main__":
    show()
