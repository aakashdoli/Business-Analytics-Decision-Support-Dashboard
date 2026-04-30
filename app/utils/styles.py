import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    
    /* Modern Cards (Glassmorphism) */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* KPI Metric Values */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 8px;
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Status Badges */
    .status-badge {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .status-healthy { background-color: #dcfce7; color: #166534; }
    .status-warning { background-color: #fef9c3; color: #854d0e; }
    .status-danger { background-color: #fee2e2; color: #991b1b; }
    
    /* AI Co-Pilot Chat Styling */
    .chat-bubble {
        background: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, delta=None, status="healthy"):
    delta_html = f'<span style="color: {"#166534" if "+" in str(delta) else "#991b1b"}; font-size: 0.875rem;">{delta}</span>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
