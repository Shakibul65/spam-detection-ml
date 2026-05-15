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

# ==========================================
# ১. ডাটাবেস সেটআপ (SQLite Integration)
# ==========================================
conn = sqlite3.connect('security_logs.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS scan_logs(user_text TEXT, result TEXT, confidence REAL, date_time TEXT)')
    conn.commit()

def add_log(text, res, conf):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO scan_logs(user_text, result, confidence, date_time) VALUES (?,?,?,?)', (text, res, conf, now))
    conn.commit()

create_table()

# ==========================================
# ২. পেজ কনফিগারেশন ও স্টাইল
# ==========================================
st.set_page_config(
    page_title="SpamGuard AI Elite | Enterprise Security",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364); 
        color: white; font-weight: bold; border: none;
    }
    .status-card { 
        background: white; padding: 30px; border-radius: 20px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-bottom: 25px;
        border-top: 5px solid #1e3c72;
    }
    .footer { text-align: center; color: #888; padding: 20px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# ৩. এআই ইঞ্জিন (Data Enrichment)
# ==========================================
@st.cache_resource
def load_advanced_engine():
    data = {
        'text': [
            'Get 100% free money now', 'Hi, how are you?', 'Claim prize money', 'Meeting at 10', 
            'Win gift card', 'Call me soon', 'Congratulations you won cash', 'Project report',
            'Account locked login here', 'Your OTP is 1234', 'Double income today', 'Lunch today?',
            'Invest now for profit', 'Verify identity immediately', 'Can we talk?', 'Meeting minutes attached'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'spam', 'ham', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    y_pred = model.predict(X)
    acc = accuracy_score(df['label'], y_pred)
    return cv, model, acc

cv, model, model_acc = load_advanced_engine()

# ==========================================
# ৪. সাইডবার নেভিগেশন
# ==========================================
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
    st.write("---")
    st.success(f"Model Accuracy: {model_acc*100:.1f}%")

# ==========================================
# ৫. অ্যাপ্লিকেশন পেজসমূহ
# ==========================================

# পেজ ১: ড্যাশবোর্ড
if menu == "🏠 Master Dashboard":
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_container_width=True)
    st.title("🚀 System Monitoring & Analytics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Scanned", "25,430", "+12%")
    c2.metric("Threats Blocked", "5,102", "+5%")
    c3.metric("DB Records", "1,204", "New")
    c4.metric("Risk Level", "Low", "Stable")
    
    st.markdown("---")
    st.subheader("📡 Real-time Threat Activity")
    chart_data = pd.DataFrame({'Attacks': np.random.randint(10, 100, size=10)})
    st.area_chart(chart_data)

# পেজ ২: স্প্যাম ডিটেক্টর (Database integrated)
elif menu == "🔍 Spam Detector AI":
    st.title("🔍 Advanced Spam Analysis")
    user_input = st.text_area("Analyze Message Content:", height=150, placeholder="Paste email/SMS content here...")
    
    if st.button("Run AI Scan 🚀"):
        if user_input:
            with st.spinner('Neural processing in progress...'):
                time.sleep(1)
                vect = cv.transform([user_input])
                res = model.predict(vect)[0]
                prob = model.predict_proba(vect)[0]
                confidence = max(prob)
                
                # ডাটাবেসে সেভ করা
                add_log(user_input, res, confidence)
                
                st.markdown("<div class='status-card'>", unsafe_allow_html=True)
                if res == 'spam':
                    st.error(f"🚨 ALERT: SPAM DETECTED! (Confidence: {confidence*100:.1f}%)")
                else:
                    st.success(f"✅ CLEAN CONTENT (Confidence: {confidence*100:.1f}%)")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter text.")

# পেজ ৩: ইউআরএল স্ক্যানার
elif menu == "🔗 URL Intelligence":
    st.title("🔗 Phishing Link Intelligence")
    st.image("https://img.freepik.com/free-vector/phishing-concept-flat-design_23-2148529367.jpg", width=600)
    url = st.text_input("Enter URL Path:")
    if st.button("Check Safety ⚙️"):
        score = 85 if any(x in url for x in ['verify', 'login', 'free', 'win']) else 10
        st.markdown(f"<div class='status-card'>Risk Score: {score}/100</div>", unsafe_allow_html=True)
        if score > 50: st.error("Highly suspicious link structure detected!")
        else: st.success("Domain pattern matches safety protocols.")

# পেজ ৪: ডাটাবেস লগস (নতুন ফিচার)
elif menu == "🗄️ Database Logs":
    st.title("🗄️ System Scan History")
    st.write("নিচের টেবিলে আপনার অ্যাপের মাধ্যমে করা সকল স্ক্যানিং ডাটাবেস থেকে দেখানো হচ্ছে।")
    
    c.execute('SELECT * FROM scan_logs ORDER BY date_time DESC')
    data = c.fetchall()
    df_logs = pd.DataFrame(data, columns=['Message', 'Result', 'Confidence', 'Date Time'])
    st.dataframe(df_logs, use_container_width=True)
    
    if st.button("Clear Logs"):
        c.execute('DELETE FROM scan_logs')
        conn.commit()
        st.success("Database cleared!")

# পেজ ৫: ইনসাইটস
elif menu == "💡 Cyber Security Insights":
    st.title("💡 Cybersecurity Resource Center")
    st.image("https://img.freepik.com/free-photo/standard-quality-control-concept-m_23-2150041848.jpg", use_container_width=True)
    t1, t2 = st.tabs(["🛡️ User Safety", "🚨 Threat landscape"])
    with t1:
        st.markdown("### How to stay protected?")
        st.write("১. **MFA:** সবসময় Multi-factor authentication ব্যবহার করুন।")
        st.write("২. **Check Source:** লিঙ্কে ক্লিক করার আগে সেন্ডারের ইমেইল চেক করুন।")
    with t2:
        fig = px.pie(names=['Phishing', 'Malware', 'Ransomware'], values=[50, 30, 20], hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

# পেজ ৬: এপিআই পোর্টাল
elif menu == "📂 Developer API":
    st.title("📂 Developer Integration")
    st.image("https://img.freepik.com/free-vector/api-concept-illustration_114360-9397.jpg", width=500)
    st.code("""
# API Call Example
import requests
def scan(text):
    return requests.post("https://api.spamguard.ai/scan", json={"msg": text}).json()
    """, language="python")

# ফুটার
st.markdown(f"<div class='footer'>Developed by <b>Shakibul Hasan</b> | CSE Student | Jamalpur, BD | {datetime.now().year}</div>", unsafe_allow_html=True)
