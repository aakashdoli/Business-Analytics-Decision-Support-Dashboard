import streamlit as st
import os
from app.etl.pipeline import ETLPipeline
from app.analytics.kpi_engine import KPIEngine
from app.analytics.anomaly_detection import AnomalyEngine
from app.forecasting.engine import ForecastingEngine

st.set_page_config(page_title="Data Management", layout="wide")

def show():
    st.title("⚙️ Data Management & ETL Center")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload New Operational Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            # Save temporary file
            with open("data/temp_upload.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if st.button("Run ETL Pipeline"):
                with st.spinner("Processing data..."):
                    try:
                        pipeline = ETLPipeline()
                        count = pipeline.process_csv("data/temp_upload.csv")
                        st.success(f"Successfully ingested {count} records!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with col2:
        st.subheader("Engine Controls")
        st.info("Trigger analytics engines to update KPIs, detect anomalies, and generate forecasts.")
        
        if st.button("Update All Analytics"):
            with st.spinner("Running Engines..."):
                try:
                    # Run KPI Engine
                    kpi = KPIEngine()
                    kpi.calculate_all_kpis()
                    st.write("✅ KPIs Calculated")
                    
                    # Run Anomaly Engine
                    anomaly = AnomalyEngine()
                    anomaly.detect_anomalies()
                    st.write("✅ Anomalies Detected")
                    
                    # Run Forecast Engine
                    forecast = ForecastingEngine()
                    forecast.generate_forecasts()
                    st.write("✅ Forecasts Generated")
                    
                    st.success("All engines completed successfully!")
                except Exception as e:
                    st.error(f"Engine Error: {e}")

if __name__ == "__main__":
    show()
