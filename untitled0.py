import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import sqlite3
from datetime import datetime
import time

# ১. ডাটাবেস ফাংশন (SQLite)
def get_db_connection():
    conn = sqlite3.connect('security_logs.db', check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS scan_logs(message TEXT, status TEXT, score REAL, timestamp TEXT)')
    conn.commit()
    conn.close()

init_db()

# ২. পেজ সেটআপ
st.set_page_config(page_title="SpamGuard Pro | Security Suite", page_icon="🛡️", layout="wide")

# ৩. কাস্টম ডিজাইন (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3b4e, #2e3b4e); color: white; }
    .stButton>button { width: 100%; border-radius: 8px; background: #1e3c72; color: white; border: none; height: 3em; }
    .status-box { padding: 20px; border-radius: 15px; background: white; border-left: 5px solid #1e3c72; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# ৪. এআই মডেল লোড
@st.cache_resource
def train_model():
    data = {
        'text': ['Win money', 'Hello friend', 'Claim reward', 'Call me', 'Free gift', 'Project update', 'Urgent verify', 'Lunch tomorrow'],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model

cv, model = train_model()

# ৫. সাইডবার নেভিগেশন
with st.sidebar:
    st.title("🛡️ SpamGuard Pro")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("### Dev: Shakibul Hasan")
    st.caption("Computer Science & Engineering")
    st.markdown("---")
    menu = st.radio("Applications", [
        "🏠 Master Dashboard", 
        "🔍 Spam Detector AI", 
        "🔗 URL Intelligence", 
        "📁 Batch Processing",
        "🗄️ Database Logs",
        "💡 Cyber Security Insights",
        "📂 Developer API"
    ])
    st.markdown("---")
    st.success("System Status: Online")

# ৬. অ্যাপ্লিকেশন লজিক
if menu == "🏠 Master Dashboard":
    st.title("🚀 Enterprise Dashboard")
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Threats Detected", "1,240", "+5%")
    c2.metric("Safe Messages", "10,430", "+12%")
    c3.metric("System Health", "99.9%", "Stable")
    
    st.subheader("Weekly Analytics")
    st.line_chart(np.random.randn(10, 2))

elif menu == "🔍 Spam Detector AI":
    st.title("🔍 Advanced Spam Guard")
    user_text = st.text_area("Enter Message:", placeholder="Type or paste here...")
    if st.button("Analyze Now"):
        if user_text:
            with st.spinner("Processing..."):
                time.sleep(1)
                vect = cv.transform([user_text])
                prediction = model.predict(vect)[0]
                prob = model.predict_proba(vect)[0]
                score = max(prob) * 100
                
                # ডাটাবেসে সেভ
                conn = get_db_connection()
                c = conn.cursor()
                c.execute('INSERT INTO scan_logs VALUES (?,?,?,?)', (user_text, prediction, score, datetime.now()))
                conn.commit()
                conn.close()
                
                st.markdown("<div class='status-box'>", unsafe_allow_html=True)
                if prediction == 'spam':
                    st.error(f"🚨 ALERT: SPAM DETECTED! (Confidence: {score:.1f}%)")
                else:
                    st.success(f"✅ MESSAGE IS SAFE (Confidence: {score:.1f}%)")
                st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🔗 URL Intelligence":
    st.title("🔗 Phishing Link Intelligence")
    url = st.text_input("Enter URL:")
    if st.button("Scan Link"):
        risk = 85 if any(x in url for x in ['login', 'verify', 'free']) else 10
        st.write(f"### Risk Score: {risk}/100")
        if risk > 50: st.error("Suspicious Link!")
        else: st.success("Safe Link Pattern.")

elif menu == "🗄️ Database Logs":
    st.title("🗄️ System Scan History")
    conn = get_db_connection()
    df_logs = pd.read_sql_query("SELECT * FROM scan_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df_logs, use_container_width=True)
    if st.button("Clear History"):
        conn.execute("DELETE FROM scan_logs")
        conn.commit()
        st.rerun()
    conn.close()

elif menu == "💡 Cyber Security Insights":
    st.title("💡 Safety Intelligence")
    st.image("https://img.freepik.com/free-photo/standard-quality-control-concept-m_23-2150041848.jpg", use_container_width=True)
    st.markdown("""
    - **Verify Identity:** Never share OTP or passwords.
    - **Check Links:** Always look for HTTPS in the URL.
    - **Report Spam:** Help the AI learn by reporting suspicious content.
    """)

elif menu == "📂 Developer API":
    st.title("📂 Integration Portal")
    st.code("""
import requests
def scan_api(text):
    return requests.post("https://api.spamguard.pro/scan", json={"msg": text}).json()
    """, language="python")

# ফুটার
st.markdown(f"<div style='text-align: center; margin-top: 50px; color: #888;'>Developed by **Shakibul Hasan** | CSE | {datetime.now().year}</div>", unsafe_allow_html=True)
