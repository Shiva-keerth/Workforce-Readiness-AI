"""
helpers.py - Utility Functions
===============================
Data persistence, password hashing, email OTP verification,
and other shared utility functions for the platform.
"""

import pandas as pd
import hashlib
import smtplib
import random
from email.mime.text import MIMEText
from config import USER_FILE, DATA_FILE, SENDER_EMAIL, EMAIL_AUTH_VAR
import streamlit as st


def init_db():
    """Initialize the user database CSV if it doesn't exist."""
    try:
        pd.read_csv(USER_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Email", "Password", "Role", "Employee_ID"])
        df.to_csv(USER_FILE, index=False)


def hash_password(password):
    """Hash a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def send_otp_email(receiver_email, otp):
    """
    Send a 6-digit OTP verification code via SMTP.
    Falls back to printing the OTP in the terminal for development.
    """
    try:
        msg = MIMEText(f"Your Workforce Portal verification code is: {otp}")
        msg['Subject'] = 'Portal Registration OTP'
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, EMAIL_AUTH_VAR)
        server.sendmail(SENDER_EMAIL, [receiver_email], msg.as_string())
        server.quit()
        return True
    except Exception:
        print(f"\n⚠️ EMAIL FAILED. Developer Mode OTP for {receiver_email} is: {otp}\n")
        return False


def save_data():
    """Persist the current dataframe back to the CSV file."""
    st.session_state.df.to_csv(DATA_FILE, index=False)


def generate_otp():
    """Generate a random 6-digit OTP string."""
    return str(random.randint(100000, 999999))
