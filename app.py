"""
Workforce Readiness AI Platform
================================
Main application entry point.
Routes authenticated users to their role-specific dashboards.

Author: Shiva Keerth G
"""

import streamlit as st
import pandas as pd
from config import DATA_FILE, apply_theme
from helpers import init_db
from auth import render_auth_page
from hr_portal import render_hr_portal
from intern_portal import render_intern_portal

# ==========================================
# 🚀 APPLICATION BOOTSTRAP
# ==========================================
st.set_page_config(page_title="Workforce Readiness Platform", layout="wide")
apply_theme()
init_db()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 🔀 ROUTING LOGIC
# ==========================================
if not st.session_state.logged_in:
    render_auth_page()
else:
    # Load the workforce dataset
    if "df" not in st.session_state:
        try:
            st.session_state.df = pd.read_csv(DATA_FILE)
        except FileNotFoundError:
            st.error(f"Cannot find {DATA_FILE}")
            st.stop()

    df = st.session_state.df

    # Render sidebar profile
    with st.sidebar:
        st.markdown("### 👤 Profile")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Role:** {st.session_state.role}")
        if st.session_state.role == "Intern":
            st.write(f"**ID:** {st.session_state.emp_id}")
        st.divider()

    # Route to the correct portal
    if st.session_state.role == "HR":
        render_hr_portal(df)
    elif st.session_state.role == "Intern":
        render_intern_portal(df)

    # Logout button
    with st.sidebar:
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
