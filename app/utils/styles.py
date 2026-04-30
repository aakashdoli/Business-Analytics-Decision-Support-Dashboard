import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* REMOVE ALL GRADIENTS FROM NAV (Targeting all potential containers) */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNav"] > div {
        background-image: none !important;
        background-color: transparent !important;
    }
    
    [data-testid="stSidebarNav"]::before, 
    [data-testid="stSidebarNav"]::after,
    [data-testid="stSidebarNav"] > div::before,
    [data-testid="stSidebarNav"] > div::after {
        content: none !important;
        display: none !important;
        background: none !important;
        background-image: none !important;
    }

    /* HIGH CONTRAST NAV LINKS */
    [data-testid="stSidebarNav"] a,
    [data-testid="stSidebarNav"] a * {
        background-color: transparent !important;
        color: #ffffff !important;
        opacity: 1 !important;
    }
    
    [data-testid="stSidebarNav"] span {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        opacity: 1 !important;
    }
    /* Active Link Highlight */
    section[data-testid="stSidebarNav"] li div a[aria-current="page"] {
        background-color: rgba(59, 130, 246, 0.2) !important;
        border-radius: 8px;
    }
    
    section[data-testid="stSidebarNav"] li div a:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
    }

    /* Icons */
    [data-testid="stSidebarNav"] svg {
        fill: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #f8fafc;
    }

    /* Style the Logout Button */
    .st-emotion-cache-79elbk { /* Custom selector for logout button */
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    .st-emotion-cache-79elbk:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: white !important;
    }
    
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
