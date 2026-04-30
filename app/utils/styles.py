import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===================== GLOBAL RESET ===================== */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide default Streamlit sidebar completely */
    [data-testid="stSidebar"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }

    /* Full-width main container */
    .block-container {
        padding: 1rem 2rem 2rem 2rem !important;
        max-width: 100% !important;
    }

    /* ===================== TOP NAV BAR ===================== */
    .enterprise-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 0.85rem 2rem;
        border-bottom: 1px solid rgba(79, 70, 229, 0.3);
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(79, 70, 229, 0.15);
    }
    .nav-brand {
        font-size: 1.1rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
    }
    .nav-brand .accent { color: #818CF8; }
    .nav-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 500;
    }
    .live-dot {
        width: 8px; height: 8px;
        background: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 6px #10B981, 0 0 12px rgba(16,185,129,0.5);
        animation: live-pulse 2s infinite;
    }
    @keyframes live-pulse {
        0%   { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70%  { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* ===================== NAV BUTTONS ===================== */
    .stButton > button {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(51, 65, 85, 0.8) !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    .stButton > button:hover {
        background: rgba(79, 70, 229, 0.2) !important;
        border-color: rgba(79, 70, 229, 0.6) !important;
        color: #A5B4FC !important;
        box-shadow: 0 0 12px rgba(79, 70, 229, 0.2) !important;
        transform: translateY(-1px) !important;
    }

    /* ===================== KPI METRIC CARDS ===================== */
    .kpi-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #4F46E5, #818CF8, #4F46E5);
        border-radius: 16px 16px 0 0;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(79, 70, 229, 0.2), 0 4px 16px rgba(0,0,0,0.4);
        border-color: rgba(79, 70, 229, 0.4);
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
        letter-spacing: -0.03em;
    }
    .kpi-delta-positive { font-size: 0.8rem; color: #10B981; font-weight: 600; margin-top: 0.35rem; }
    .kpi-delta-negative { font-size: 0.8rem; color: #EF4444; font-weight: 600; margin-top: 0.35rem; }
    .kpi-delta-neutral  { font-size: 0.8rem; color: #64748B; font-weight: 600; margin-top: 0.35rem; }

    /* ===================== INCIDENT / ALERT CARDS ===================== */
    .incident-critical {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 4px solid #EF4444;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.1);
    }
    .incident-warning {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 4px solid #F59E0B;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.5rem;
    }
    .incident-info {
        background: rgba(79, 70, 229, 0.08);
        border: 1px solid rgba(79, 70, 229, 0.3);
        border-left: 4px solid #4F46E5;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.5rem;
    }
    .incident-success {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 4px solid #10B981;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.5rem;
    }
    .incident-text { font-size: 0.82rem; color: #CBD5E1; font-weight: 500; }
    .incident-time { font-size: 0.72rem; color: #475569; margin-top: 0.2rem; }

    /* ===================== SECTION HEADERS ===================== */
    .section-header {
        font-size: 0.7rem;
        font-weight: 700;
        color: #4F46E5;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 1rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(79, 70, 229, 0.2);
    }

    /* ===================== GLASSMORPHISM PANEL ===================== */
    .glass-panel {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ===================== LIVE FEED ===================== */
    .live-feed-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid rgba(51, 65, 85, 0.3);
        font-size: 0.82rem;
    }
    .live-feed-item:last-child { border-bottom: none; }
    .feed-icon { font-size: 1rem; flex-shrink: 0; margin-top: 0.1rem; }
    .feed-content { flex: 1; color: #CBD5E1; }
    .feed-time { font-size: 0.7rem; color: #475569; white-space: nowrap; }

    /* ===================== SYSTEM STATUS BADGE ===================== */
    .sys-badge {
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .sys-badge-healthy { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); }
    .sys-badge-warning { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3); }
    .sys-badge-critical { background: rgba(239,68,68,0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); box-shadow: 0 0 10px rgba(239,68,68,0.2); }

    /* ===================== SCROLLBAR ===================== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0B0F19; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #4F46E5; }

    /* ===================== STREAMLIT OVERRIDES ===================== */
    [data-testid="stMetricLabel"] { color: #64748B !important; font-size: 0.72rem !important; }
    [data-testid="stMetricValue"] { color: #F8FAFC !important; }
    [data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

    /* Tab styling */
    [data-testid="stTabs"] [role="tab"] {
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #818CF8 !important;
        border-bottom-color: #4F46E5 !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        border-color: rgba(51, 65, 85, 0.8) !important;
        color: #F8FAFC !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(51, 65, 85, 0.6) !important;
        border-radius: 12px !important;
    }

    /* Page title */
    h1 { 
        font-weight: 800 !important; 
        letter-spacing: -0.03em !important; 
        color: #F8FAFC !important;
        font-size: 1.8rem !important;
    }
    h2, h3 { color: #E2E8F0 !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = None):
    """Render a premium dark glassmorphism KPI metric card."""
    delta_html = ""
    if delta:
        is_positive = "+" in delta and "-" not in delta.split("+")[0]
        delta_class = "kpi-delta-positive" if is_positive else "kpi-delta-negative"
        delta_html = f'<div class="{delta_class}">▲ {delta}' if is_positive else f'<div class="{delta_class}">▼ {delta}'
        delta_html += "</div>"

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
