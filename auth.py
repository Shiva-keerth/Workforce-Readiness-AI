"""
auth.py - Authentication Module
================================
Handles user login, registration, and OTP-based email verification.
Implements secure SHA-256 password hashing and session state management.
"""

import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
from config import USER_FILE, load_lottieurl
from helpers import hash_password, send_otp_email, init_db, generate_otp


def render_auth_page():
    """Render the login and registration interface."""
    init_db()

    if "otp" not in st.session_state:
        st.session_state.otp = None
    if "register_data" not in st.session_state:
        st.session_state.register_data = None

    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        lottie_login = load_lottieurl(
            "https://lottie.host/880b957e-dbdf-43e6-bf25-46a4da90635f/tXq8v6KXY8.json"
        )
        if lottie_login:
            st_lottie(lottie_login, height=150, key="login_anim")

        st.title("🔐 Workforce Portal")
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            _render_login_tab()

        with tab2:
            _render_register_tab()


def _render_login_tab():
    """Render the login form and handle authentication."""
    login_email = st.text_input("Email", key="login_email")
    login_pass = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", type="primary", use_container_width=True):
        users_df = pd.read_csv(USER_FILE)
        hashed_input = hash_password(login_pass)
        user = users_df[
            (users_df['Email'] == login_email) & (users_df['Password'] == hashed_input)
        ]

        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.role = user.iloc[0]['Role']
            st.session_state.user_email = user.iloc[0]['Email']
            st.session_state.emp_id = user.iloc[0]['Employee_ID']
            st.rerun()
        else:
            st.error("Invalid Email or Password")


def _render_register_tab():
    """Render the registration form with OTP verification."""
    reg_email = st.text_input("Work Email")
    reg_pass = st.text_input("Password", type="password")
    reg_role = st.selectbox("Register as:", ["Intern", "HR"])

    reg_emp_id = "N/A"
    if reg_role == "Intern":
        reg_emp_id = st.text_input("Your Employee ID (e.g., EMP_00001)")

    if st.button("Send Verification Code", use_container_width=True):
        users_df = pd.read_csv(USER_FILE)
        if reg_email in users_df['Email'].values:
            st.error("Email is already registered!")
        elif reg_role == "Intern" and not reg_emp_id:
            st.error("Interns must provide their Employee ID.")
        else:
            st.session_state.otp = generate_otp()
            st.session_state.register_data = {
                "Email": reg_email,
                "Password": hash_password(reg_pass),
                "Role": reg_role,
                "Employee_ID": reg_emp_id,
            }
            if send_otp_email(reg_email, st.session_state.otp):
                st.success("OTP sent to your email!")
            else:
                st.warning("Check your terminal for the OTP!")

    if st.session_state.otp:
        entered_otp = st.text_input("Enter 6-digit OTP", max_chars=6)
        if st.button("Verify & Register", type="primary"):
            if entered_otp == st.session_state.otp:
                new_user = pd.DataFrame([st.session_state.register_data])
                new_user.to_csv(USER_FILE, mode='a', header=False, index=False)
                st.success("Account created! You can now Login.")
                st.session_state.otp = None
            else:
                st.error("Incorrect OTP.")
