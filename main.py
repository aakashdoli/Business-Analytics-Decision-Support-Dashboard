import streamlit as st
import streamlit_authenticator as stauth
import os
from dotenv import load_dotenv
from app.utils.styles import apply_custom_styles

load_dotenv()

st.set_page_config(
    page_title="Enterprise Analytics | Co-Pilot",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_styles()

# Auth Configuration
names = ["Executive Admin"]
usernames = ["admin"]
passwords = ["admin123"]
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    {'usernames': {usernames[0]: {'name': names[0], 'password': hashed_passwords[0]}}},
    "enterprise_analytics",
    "auth_key",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login(location="main")

if authentication_status:
    st.sidebar.markdown(f"### 👤 {name}")
    authenticator.logout("Logout", "sidebar")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 NAVIGATION")
    
    st.title("💎 Enterprise SaaS Dashboard")
    st.markdown("##### Welcome to your real-time business intelligence suite.")
    
    st.markdown("---")
    
    # Overview metrics in new cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Global Revenue", "$24.8M", "+14.2% MoM")
    with col2:
        st.metric("Ops Efficiency", "92.4%", "+2.1%")
    with col3:
        st.metric("Inventory Health", "Good", "Normal")
    with col4:
        st.metric("Active Regions", "4", "Stable")

    st.markdown("### 🚀 Get Started")
    st.info("Select **AI Co-Pilot** from the sidebar to ask questions about your business data directly.")

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your credentials to access the secure portal.")
