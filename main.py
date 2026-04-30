import streamlit as st
import pandas as pd
from datetime import datetime
from app.utils.styles import apply_custom_styles
from app.utils.navigation import render_top_nav
from app.database.session import SessionLocal
from app.database.models import KPIResult, AnomalyLog

st.set_page_config(
    page_title="Enterprise Intelligence Platform",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_styles()
render_top_nav()

# ── Live Operational Feed ──────────────────────────────────────────────────────
import random
import time

LIVE_EVENTS = [
    ("🔴", "critical",  "Revenue anomaly detected in APAC Operations — confidence 91.3%"),
    ("🟡", "warning",   "Forecast drift exceeded 95% confidence threshold — Revenue metric"),
    ("🟡", "warning",   "Customer Support costs increased 12.4% QoQ in EMEA"),
    ("🟢", "success",   "ETL pipeline completed — 26,280 records synced to data warehouse"),
    ("🔵", "info",      "Prophet forecasting engine refit — 3 metrics updated"),
    ("🟡", "warning",   "Inventory efficiency degraded in EMEA — Logistics delay +2.1d"),
    ("🟢", "success",   "KPI engine recalculated — Gross Margin stable at 38.4%"),
    ("🔴", "critical",  "LATAM Manufacturing cost spike — 18.7% above seasonal baseline"),
    ("🟢", "success",   "Anomaly detection sweep complete — 247 incidents logged"),
    ("🔵", "info",      "AI Co-Pilot session initialised — semantic context loaded"),
]

db = SessionLocal()
kpis = db.query(KPIResult).all()
latest_anomaly = db.query(AnomalyLog).order_by(AnomalyLog.detected_at.desc()).first()

# ── Hero Banner ────────────────────────────────────────────────────────────────
now = datetime.now().strftime("%d %b %Y • %H:%M")
health_val = next((k.value for k in kpis if k.name == "Business Health"), 78.0)
if health_val >= 75:
    badge = '<span class="sys-badge sys-badge-healthy">● HEALTHY</span>'
elif health_val >= 55:
    badge = '<span class="sys-badge sys-badge-warning">● WARNING</span>'
else:
    badge = '<span class="sys-badge sys-badge-critical">● CRITICAL</span>'

st.markdown(f"""
<div class="glass-panel" style="margin-bottom:1.5rem;">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
    <div>
      <div style="font-size:0.72rem;color:#64748B;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.4rem;">ENTERPRISE AI OPERATIONAL INTELLIGENCE</div>
      <div style="font-size:1.6rem;font-weight:800;color:#F8FAFC;letter-spacing:-.03em;">Good {('Morning' if datetime.now().hour < 12 else 'Afternoon')}, Executive Admin</div>
      <div style="font-size:.82rem;color:#64748B;margin-top:.3rem;">{now} &nbsp;|&nbsp; 4 Regions Active &nbsp;|&nbsp; 6 Departments Monitored</div>
    </div>
    <div style="display:flex;gap:.75rem;align-items:center;">
      {badge}
      <span style="font-size:.78rem;color:#64748B;">Business Health: <strong style="color:#F8FAFC;">{health_val:.1f}/95</strong></span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards Row ─────────────────────────────────────────────────────────────
if kpis:
    cols = st.columns(len(kpis))
    icon_map = {"Total Revenue": "💰", "Gross Margin": "📈", "Operating Margin": "📊",
                "Business Health": "💚", "Ops Efficiency": "⚡"}
    for i, kpi in enumerate(kpis):
        with cols[i]:
            if "Revenue" in kpi.name:
                val = f"${kpi.value/1_000_000:.2f}M"
            elif any(x in kpi.name for x in ["Margin", "Efficiency"]):
                val = f"{kpi.value:.1f}%"
            else:
                val = f"{kpi.value:.1f}"

            delta_html = ""
            if kpi.mom_growth:
                is_pos = kpi.mom_growth >= 0
                color = "#10B981" if is_pos else "#EF4444"
                arrow = "▲" if is_pos else "▼"
                delta_html = f'<div style="font-size:.8rem;color:{color};font-weight:600;margin-top:.35rem;">{arrow} {kpi.mom_growth:+.1f}% MoM</div>'

            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{icon_map.get(kpi.name,'📌')} {kpi.name}</div>
              <div class="kpi-value">{val}</div>
              {delta_html}
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main 2-col Layout ─────────────────────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="section-header">⚡ LIVE OPERATIONAL FEED</div>', unsafe_allow_html=True)

    # Simulate real-time ticking by seeding randomness off minute
    random.seed(int(time.time() // 60))
    feed_items = random.sample(LIVE_EVENTS, k=7)

    type_class = {"critical": "incident-critical", "warning": "incident-warning",
                  "info": "incident-info", "success": "incident-success"}
    minutes_ago = [1, 2, 4, 7, 11, 18, 26]
    for idx, (icon, severity, msg) in enumerate(feed_items):
        mins = minutes_ago[idx]
        ago = f"{mins}m ago" if mins < 60 else f"{mins//60}h ago"
        st.markdown(f"""
        <div class="{type_class[severity]}">
          <div class="incident-text">{icon} &nbsp;{msg}</div>
          <div class="incident-time">🕐 {ago}</div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-header">🖥 SYSTEM STATUS</div>', unsafe_allow_html=True)

    systems = [
        ("ETL Pipeline",       "healthy", "Last run: 2m ago"),
        ("KPI Engine",         "healthy", "5 metrics live"),
        ("Prophet Forecaster", "healthy", "3 metrics tracked"),
        ("Isolation Forest",   "warning", "Refit pending"),
        ("AI Co-Pilot",        "healthy", "Context loaded"),
        ("Data Warehouse",     "healthy", "26,280 records"),
    ]
    for sys_name, status, detail in systems:
        badge_cls = f"sys-badge sys-badge-{status}"
        dot = "●"
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
                    padding:.55rem 0;border-bottom:1px solid rgba(51,65,85,.3);">
          <div>
            <div style="font-size:.83rem;font-weight:600;color:#CBD5E1;">{sys_name}</div>
            <div style="font-size:.7rem;color:#475569;">{detail}</div>
          </div>
          <span class="{badge_cls}">{dot} {status.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    # Active anomaly count
    if latest_anomaly:
        st.markdown(f"""
        <div class="incident-critical" style="margin-top:1rem;">
          <div class="incident-text">🔴 Latest: {latest_anomaly.description[:60]}...</div>
          <div class="incident-time">{latest_anomaly.date}</div>
        </div>
        """, unsafe_allow_html=True)

db.close()
