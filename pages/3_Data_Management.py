import streamlit as st
import os
import pandas as pd
from app.etl.pipeline import ETLPipeline
from app.analytics.kpi_engine import KPIEngine
from app.analytics.anomaly_detection import AnomalyEngine
from app.forecasting.engine import ForecastingEngine
from app.utils.generate_data import generate_enterprise_data
from app.utils.styles import apply_custom_styles

st.set_page_config(page_title="Data Management", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()

def show():
    st.title("⚙️ Operations Control Center")
    st.markdown("##### ETL Pipelines, Data Management & Engine Execution")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Data Ingestion Pipeline")
        st.info("Upload raw operational extracts for ETL processing.")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            # Save temporary file
            os.makedirs("data", exist_ok=True)
            with open("data/temp_upload.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if st.button("▶️ Execute ETL Pipeline", type="primary"):
                with st.status("Executing ETL Pipeline...", expanded=True) as status:
                    try:
                        st.write("Initializing pipeline...")
                        pipeline = ETLPipeline()
                        st.write("Validating and cleaning dataset...")
                        count = pipeline.process_csv("data/temp_upload.csv")
                        st.write("Writing to Operational Data Store...")
                        status.update(label=f"ETL Complete: Ingested {count} records.", state="complete", expanded=False)
                        st.success(f"Successfully synced {count} records to database.")
                    except Exception as e:
                        status.update(label="ETL Failed", state="error")
                        st.error(f"Pipeline Error: {e}")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("🧪 Enterprise Data Generator")
        st.warning("Warning: Generating new data will overwrite existing data patterns.")
        gen_years = st.slider("Years of Data to Generate", min_value=1, max_value=5, value=3)
        if st.button("Generate Synthetic Enterprise Dataset"):
            with st.spinner(f"Generating {gen_years} years of multi-departmental data..."):
                generate_enterprise_data(num_years=gen_years)
                st.success("Dataset generated in `data/enterprise_operations.csv`. You can now execute the ETL Pipeline.")

    with col2:
        st.subheader("🧠 Analytics Engine Execution")
        st.markdown("Manually trigger downstream analytics engines to update the dashboard.")
        
        # Engine Control Panel UI
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h4>Batch Execution</h4>
            <p style="color: #64748B;">Runs KPI Engine, Isolation Forests, and Prophet Forecasting sequentially.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Run Full Analytics Suite", type="primary", use_container_width=True):
            with st.status("Executing Analytics Suite...", expanded=True) as status:
                try:
                    # Run KPI Engine
                    st.write("⏳ Calculating Enterprise KPIs...")
                    kpi = KPIEngine()
                    kpi.calculate_all_kpis()
                    st.write("✅ KPIs Calculated")
                    
                    # Run Anomaly Engine
                    st.write("⏳ Running Isolation Forest Anomaly Detection...")
                    anomaly = AnomalyEngine()
                    anomaly.detect_anomalies()
                    st.write("✅ Incidents Detected")
                    
                    # Run Forecast Engine
                    st.write("⏳ Generating Prophet Multi-Metric Forecasts...")
                    forecast = ForecastingEngine()
                    forecast.generate_forecasts()
                    st.write("✅ Forecasts Generated")
                    
                    status.update(label="Analytics Suite Execution Complete", state="complete", expanded=True)
                    st.success("Dashboard successfully updated with latest ML insights.")
                except Exception as e:
                    status.update(label="Execution Failed", state="error")
                    st.error(f"Engine Error: {e}")
                    
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("📑 Enterprise Reporting")
        st.info("Generate and download the latest Executive Summary Report.")
        
        if st.button("📄 Generate Executive Report", use_container_width=True):
            from app.reporting.exporter import generate_executive_report
            filepath = generate_executive_report()
            with open(filepath, "r") as f:
                report_data = f.read()
            
            st.success(f"Report Generated: {os.path.basename(filepath)}")
            st.download_button(
                label="⬇️ Download Markdown Report",
                data=report_data,
                file_name=os.path.basename(filepath),
                mime="text/markdown",
                use_container_width=True
            )

if __name__ == "__main__":
    show()
