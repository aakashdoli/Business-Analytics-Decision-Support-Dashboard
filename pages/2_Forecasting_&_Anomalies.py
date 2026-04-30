import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app.database.session import SessionLocal
from app.database.models import ForecastResult, AnomalyLog, OperationalData

from app.utils.styles import apply_custom_styles

st.set_page_config(page_title="Forecasting & Anomalies", layout="wide")
apply_custom_styles()

def show():
    st.title("🔮 Forecasting & Anomaly Detection")
    db = SessionLocal()
    
    tab1, tab2 = st.tabs(["Revenue Forecast", "Anomaly Logs"])
    
    with tab1:
        st.subheader("30-Day Revenue Projection")
        forecasts = db.query(ForecastResult).order_by(ForecastResult.forecast_date).all()
        
        if forecasts:
            f_df = pd.DataFrame([{
                'date': f.forecast_date,
                'predicted': f.predicted_value,
                'lower': f.lower_bound,
                'upper': f.upper_bound
            } for f in forecasts])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=f_df['date'], y=f_df['predicted'], name='Forecast'))
            if f_df['upper'].notnull().any():
                fig.add_trace(go.Scatter(x=f_df['date'], y=f_df['upper'], fill=None, mode='lines', line_color='rgba(0,0,0,0)', showlegend=False))
                fig.add_trace(go.Scatter(x=f_df['date'], y=f_df['lower'], fill='tonexty', mode='lines', line_color='rgba(0,0,0,0)', name='Confidence Interval'))
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No forecast data available. Run the forecasting engine from the Data Center.")

    with tab2:
        st.subheader("Detected System Anomalies")
        anomalies = db.query(AnomalyLog).order_by(AnomalyLog.date.desc()).all()
        
        if anomalies:
            a_df = pd.DataFrame([{
                'Date': a.date,
                'Metric': a.metric_name,
                'Value': a.observed_value,
                'Confidence': a.confidence_score,
                'Severity': a.severity,
                'Description': a.description
            } for a in anomalies])
            
            st.dataframe(a_df, use_container_width=True)
            
            # Anomaly Scatter Plot
            raw_data = db.query(OperationalData).all()
            raw_df = pd.DataFrame([{'date': d.date, 'revenue': d.revenue} for d in raw_data])
            
            fig = px.scatter(raw_df, x='date', y='revenue', title="Revenue Anomalies")
            # Highlight anomalies
            anomaly_dates = a_df[a_df['Metric'] == 'revenue']['Date'].tolist()
            anomaly_points = raw_df[raw_df['date'].isin(anomaly_dates)]
            
            fig.add_trace(go.Scatter(x=anomaly_points['date'], y=anomaly_points['revenue'], 
                                     mode='markers', marker=dict(color='red', size=10), name='Anomaly'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No anomalies detected in the current dataset.")

    db.close()

if __name__ == "__main__":
    show()
