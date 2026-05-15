import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ১. পেজ সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. চোখের জন্য আরামদায়ক ডার্ক থিম (Midnight Blue UI)
st.markdown("""
    <style>
    .stApp {
        background: #0f172a; 
        color: #e2e8f0;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }

    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px;
        border-radius: 24px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border: none;
        color: white;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }

    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
    }

    .footer-text {
        color: #94a3b8;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইডবার (Branding Update: CSE Student)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Developed By:**")
    st.info("**Shakibul Hasan**\n\
