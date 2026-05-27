"""
config.py - Application Configuration & Premium UI Theme
=========================================================
Centralized configuration for the Workforce Readiness AI Platform.
Contains all CSS styling, animation definitions, and global constants.
"""

import streamlit as st
import time
import requests

# ==========================================
# 📁 FILE PATHS & GLOBAL CONSTANTS
# ==========================================
USER_FILE = "users.csv"
DATA_FILE = "intern dataset.csv"

SENDER_EMAIL = "your_email@gmail.com"
EMAIL_AUTH_VAR = "your_sixteen_digit_app_str"


# ==========================================
# 🎨 EMBEDDED PREMIUM UI CSS (Glassmorphism)
# ==========================================
CUSTOM_CSS = """
<style>
/* Hide default header/footer safely */
[data-testid="stHeader"] {visibility: hidden;}
footer {visibility: hidden;}

/* Safe Background Gradient */
.stApp {
    background: linear-gradient(135deg, #0f121b 0%, #171c2b 100%);
    color: #ffffff;
}

/* Animated Blobs - Fixed positioning and pointer-events:none prevents blocking UI */
.stApp::before {
    content: "";
    position: fixed;
    top: -10%; left: -10%;
    width: 50vw; height: 50vh;
    background: radial-gradient(circle, rgba(76, 175, 80, 0.12) 0%, rgba(0,0,0,0) 70%);
    animation: floatBlob 15s infinite alternate ease-in-out;
    z-index: 0;
    pointer-events: none; 
}

.stApp::after {
    content: "";
    position: fixed;
    bottom: -10%; right: -10%;
    width: 60vw; height: 60vh;
    background: radial-gradient(circle, rgba(63, 81, 181, 0.12) 0%, rgba(0,0,0,0) 70%);
    animation: floatBlob2 20s infinite alternate ease-in-out;
    z-index: 0;
    pointer-events: none;
}

/* Ensure the actual app content stays above the animated background */
[data-testid="stAppViewBlockContainer"] {
    position: relative;
    z-index: 1;
}

@keyframes floatBlob {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(100px, 100px) scale(1.2); }
}

@keyframes floatBlob2 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-100px, -150px) scale(1.1); }
}

/* Glassmorphism Cards */
[data-testid="stMetric"], [data-testid="stForm"], [data-testid="stExpander"] {
    background: rgba(30, 34, 53, 0.4) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255,255,255,0.05);
    transition: transform 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(76, 175, 80, 0.3);
}

[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
}

/* Custom Inputs & Buttons */
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background-color: rgba(0,0,0,0.3) !important;
    color: white !important;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border: 1px solid #4CAF50 !important;
    box-shadow: 0 0 10px rgba(76, 175, 80, 0.3) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4) !important;
}

/* Sidebar Glassmorphism */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.05);
    background: rgba(14, 17, 23, 0.8) !important;
    backdrop-filter: blur(20px) !important;
}
</style>
"""


# ==========================================
# ⚙️ HELPER FUNCTIONS
# ==========================================
def load_lottieurl(url: str):
    """Load a Lottie animation from a URL with a timeout."""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def stream_typing_effect(text):
    """Generator that yields words one at a time for a typing effect."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04)


def apply_theme():
    """Inject the premium CSS theme into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
