import streamlit as st
import os
from app.etl.pipeline import ETLPipeline
from app.analytics.kpi_engine import KPIEngine
from app.analytics.anomaly_detection import AnomalyEngine
from app.forecasting.engine import ForecastingEngine
from app.utils.generate_data import generate_enterprise_data
from app.utils.styles import apply_custom_styles
from app.utils.navigation import render_top_nav

st.set_page_config(page_title="Operations Control Center", layout="wide", initial_sidebar_state="collapsed")
apply_custom_styles()
render_top_nav()

st.markdown("# ⚙️ Operations Control Center")
st.markdown('<div style="font-size:.88rem;color:#64748B;margin-bottom:1.5rem;">ETL pipeline management · Analytics engine execution · Reporting</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header">📥 DATA INGESTION PIPELINE</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-panel">
      <div style="font-size:.85rem;color:#94A3B8;margin-bottom:1rem;">Upload raw operational extracts for ETL processing and ingestion into the data warehouse.</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        os.makedirs("data", exist_ok=True)
        with open("data/temp_upload.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        if st.button("▶️ Execute ETL Pipeline", type="primary"):
            with st.status("Executing ETL Pipeline...", expanded=True) as status:
                try:
                    st.write("Initialising pipeline...")
                    pipeline = ETLPipeline()
                    st.write("Validating and cleaning dataset...")
                    count = pipeline.process_csv("data/temp_upload.csv")
                    st.write("Writing to Operational Data Store...")
                    status.update(label=f"✅ ETL Complete: {count:,} records synced.", state="complete")
                    st.success(f"Successfully synced **{count:,}** records to database.")
                except Exception as e:
                    status.update(label="❌ ETL Failed", state="error")
                    st.error(f"Pipeline Error: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">🧪 SYNTHETIC DATA GENERATOR</div>', unsafe_allow_html=True)
    st.markdown("""<div class="incident-warning"><div class="incident-text">⚠️ Generating new data will overwrite existing warehouse records.</div></div>""", unsafe_allow_html=True)
    gen_years = st.slider("Years of Enterprise Data", min_value=1, max_value=5, value=3)
    if st.button("🔄 Generate Synthetic Enterprise Dataset"):
        with st.spinner(f"Generating {gen_years} years of correlated enterprise data..."):
            generate_enterprise_data(num_years=gen_years)
            st.success("Dataset written to `data/enterprise_operations.csv`. Now execute the ETL Pipeline ↑")

with col2:
    st.markdown('<div class="section-header">🧠 ANALYTICS ENGINE EXECUTION</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-panel">
      <div style="font-size:.85rem;color:#94A3B8;margin-bottom:.5rem;">Trigger the full downstream ML suite: KPI Engine → Isolation Forests → Prophet Forecasting.</div>
      <div class="incident-info"><div class="incident-text">🔵 Estimated runtime: ~45 seconds with Prophet enabled.</div></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Run Full Analytics Suite", type="primary", use_container_width=True):
        with st.status("Executing Analytics Suite...", expanded=True) as status:
            try:
                st.write("⏳ Recalculating Enterprise KPIs...")
                KPIEngine().calculate_all_kpis()
                st.write("✅ KPI Engine complete")

                st.write("⏳ Running Isolation Forest Anomaly Detection...")
                AnomalyEngine().detect_anomalies()
                st.write("✅ Incident detection complete")

                st.write("⏳ Fitting Prophet multi-metric forecasts...")
                ForecastingEngine().generate_forecasts()
                st.write("✅ Forecasts generated")

                status.update(label="✅ Analytics Suite Complete", state="complete", expanded=True)
                st.success("All engines executed. Dashboard now reflects latest insights.")
            except Exception as e:
                status.update(label="❌ Execution Failed", state="error")
                st.error(f"Engine Error: {e}")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📑 EXECUTIVE REPORTING</div>', unsafe_allow_html=True)
    if st.button("📄 Generate Executive Summary Report", use_container_width=True):
        from app.reporting.exporter import generate_executive_report
        filepath = generate_executive_report()
        with open(filepath, "r") as f:
            report_data = f.read()
        st.success(f"Report generated: `{os.path.basename(filepath)}`")
        st.download_button(
            label="⬇️ Download Markdown Report",
            data=report_data,
            file_name=os.path.basename(filepath),
            mime="text/markdown",
            use_container_width=True
        )
