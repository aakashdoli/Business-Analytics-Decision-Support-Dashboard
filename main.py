import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Simple Auth Configuration (In a real app, this would be in a DB or config file)
names = ["Admin User"]
usernames = ["admin"]
passwords = ["admin123"] # In production, use hashed passwords

# Pre-hashing passwords for the authenticator
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    {'usernames': {usernames[0]: {'name': names[0], 'password': hashed_passwords[0]}}},
    "analytics_dashboard",
    "auth_key",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login(location="main")

if authentication_status:
    st.sidebar.success(f"Welcome {name}")
    authenticator.logout("Logout", "sidebar")
    
    st.title("🚀 Business Analytics & Decision Support")
    st.markdown("---")
    
    # Navigation Instructions
    st.info("Select a page from the sidebar to begin your analysis.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", "$1.2M", "+12%")
    with col2:
        st.metric("Ops Efficiency", "85%", "+5%")
    with col3:
        st.metric("Active Anomalies", "3", "-2")

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
