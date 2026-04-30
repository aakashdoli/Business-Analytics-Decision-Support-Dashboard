import streamlit as st

def render_top_nav():
    """Renders a custom top navigation bar and hides the default Streamlit sidebar."""
    
    st.markdown("""
        <style>
            /* Hide Streamlit default sidebar and header */
            [data-testid="stSidebar"] { display: none; }
            header { display: none; }
            
            /* Custom Top Nav Styling */
            .top-nav {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background-color: #1E293B; /* Secondary Slate */
                padding: 1rem 2rem;
                border-bottom: 1px solid #334155;
                margin-top: -4rem; /* Offset Streamlit default padding */
                margin-bottom: 2rem;
                margin-left: -4rem;
                margin-right: -4rem;
            }
            .nav-brand {
                font-weight: 800;
                font-size: 1.25rem;
                color: #F8FAFC;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .nav-brand span { color: #4F46E5; }
            .nav-links {
                display: flex;
                gap: 1.5rem;
            }
            /* System Status dot */
            .status-dot {
                height: 10px;
                width: 10px;
                background-color: #10B981; /* Emerald */
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 8px #10B981;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
                70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
                100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
            }
            .sys-status {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                color: #94A3B8;
            }
        </style>
    """, unsafe_allow_html=True)

    # HTML Top Nav
    st.markdown("""
        <div class="top-nav">
            <div class="nav-brand">💎 Enterprise<span>Intelligence</span></div>
            <div class="sys-status">
                <span class="status-dot"></span> 
                Live Ops: Active
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Streamlit native horizontal routing buttons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 3])
    with col1:
        if st.button("📊 Executive Dash", use_container_width=True):
            st.switch_page("pages/1_Executive_Summary.py")
    with col2:
        if st.button("🔮 Forecast & ML", use_container_width=True):
            st.switch_page("pages/2_Forecasting_&_Anomalies.py")
    with col3:
        if st.button("⚙️ Control Center", use_container_width=True):
            st.switch_page("pages/3_Data_Management.py")
    with col4:
        if st.button("🤖 AI Co-Pilot", use_container_width=True):
            st.switch_page("pages/4_AI_Co_Pilot.py")
            
    st.markdown("<br>", unsafe_allow_html=True)
