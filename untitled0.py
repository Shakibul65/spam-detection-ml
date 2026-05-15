import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from datetime import datetime
import time

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="SpamGuard AI Elite | Security Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম সিএসএস (UI Fix)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.8em; 
        background: linear-gradient(90deg, #1e3c72, #2a5298); 
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .status-card { 
        background: white; padding: 25px; border-radius: 20px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 25px;
        border-left: 6px solid #1e3c72;
    }
    .footer { text-align: center; color: #666; padding: 30px; border-top: 1px solid #ddd; margin-top: 60px; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন লোড
@st.cache_resource
def load_advanced_engine():
    data = {
        'text': [
            'Free money now', 'Hi, how are you?', 'Claim prize money', 'Meeting at 10', 
            'Win gift card', 'Call me soon', 'Congratulations you won cash', 'Project report',
            'Account locked login here', 'Your OTP is 1234', 'Double income today', 'Lunch today?',
            'Get 100% discount', 'Can we talk?', 'Urgent: Verify identity', 'File received'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model

cv, model = load_advanced_engine()

# ৪. সাইডবার নেভিগেশন (Fixing NameError)
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("### Developer: Shakibul Hasan")
    st.caption("CSE Student | Jamalpur, BD")
    st.markdown("---")
    # 'menu' ভেরিয়েবলটি এখানে ডিফাইন করা হয়েছে
    menu = st.radio("Applications", [
        "🏠 Dashboard", 
        "🔍 Spam Detector", 
        "🔗 URL Scanner", 
        "📁 Bulk Analyzer", 
        "💡 Cybersecurity Insights",
        "📂 API & Developer Portal"
    ])
    st.markdown("---")
    st.info("System Status: Active")

# ৫. ড্যাশবোর্ড
if menu == "🏠 Dashboard":
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_container_width=True)
    st.title("🚀 Security Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Scanned", "12.5k", "+18%")
    c2.metric("Blocked", "3,402", "+12%")
    c3.metric("Sites", "842", "+25%")
    c4.metric("Risk Level", "Low", "Stable")
    
    st.markdown("---")
    st.subheader("Weekly Threat Analytics")
    st.area_chart(pd.DataFrame({'Threats': [10, 25, 15, 45, 30, 10, 5]}))

# ৬. স্প্যাম ডিটেক্টর
elif menu == "🔍 Spam Detector":
    st.title("🔍 Advanced Spam Guard")
    text_input = st.text_area("Analyze Message Content:", height=150)
    if st.button("Run AI Analysis 🚀"):
        if text_input:
            vect = cv.transform([text_input])
            res = model.predict(vect)[0]
            st.markdown("<div class='status-card'>", unsafe_allow_html=True)
            if res == 'spam': st.error("🚨 ALERT: SPAM DETECTED!")
            else: st.success("✅ CLEAN CONTENT DETECTED")
            st.markdown("</div>", unsafe_allow_html=True)

# ৭. ইউআরএল স্ক্যানার (Score Logic Explained)
elif menu == "🔗 URL Scanner":
    st.title("🔗 Phishing Link Intelligence")
    st.image("https://img.freepik.com/free-vector/phishing-concept-flat-design_23-2148529367.jpg", width=600)
    url = st.text_input("Enter URL Path:", placeholder="https://www.google.com")
    
    if st.button("Scan Link Safety ⚙️"):
        if url:
            # স্কোরিং লজিক
            score = 10 # ডিফল্ট সেফটি স্কোর
            if "verify" in url or "login" in url: score += 55
            if len(url) > 50: score += 20
            
            st.markdown(f"<div class='status-card'>Link Scanned. Risk Score: {score}/100</div>", unsafe_allow_html=True)
            if score > 50: st.error("🚨 This link looks suspicious!")
            else: st.success("✅ This link appears to be safe.")

# ৮. বাল্ক এনালাইজার
elif menu == "📁 Bulk Analyzer":
    st.title("📁 Batch Processing")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        st.success("Dataset Loaded!")
        st.button("Start Bulk Processing")

# ৯. সাইবার সিকিউরিটি ইনসাইটস (নতুন বড় কন্টেন্ট ও ছবি)
elif menu == "💡 Cybersecurity Insights":
    st.title("💡 Security Intelligence Center")
    st.image("https://img.freepik.com/free-photo/standard-quality-control-concept-m_23-2150041848.jpg", use_container_width=True)
    
    t1, t2 = st.tabs(["🛡️ Safety Tips", "📊 Threat Stats"])
    with t1:
        st.subheader("How to Stay Safe Online")
        st.write("- **2FA:** সবসময় টু-ফ্যাক্টর অথেন্টিকেশন চালু রাখুন।")
        st.write("- **Links:** অপরিচিত নম্বর থেকে আসা লিঙ্কে ক্লিক করবেন না।")
        st.write("- **Software:** আপনার ফোনের সিকিউরিটি প্যাচ আপডেট রাখুন।")
    with t2:
        st.subheader("Threat Distribution 2026")
        fig = px.pie(names=['Phishing', 'Malware', 'Others'], values=[60, 25, 15], hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

# ১০. এপিআই পোর্টাল
elif menu == "📂 API & Developer Portal":
    st.title("📂 Developer Hub")
    st.image("https://img.freepik.com/free-vector/api-concept-illustration_114360-9397.jpg", width=500)
    st.markdown("### Integration Example")
    st.code("""
import requests
# Your API Integration code here
response = requests.post("https://api.spamguard.ai/scan", json={"text": "Win $1000"})
print(response.json())
    """, language="python")

# ১১. ফুটার
st.markdown(f"<div class='footer'>Developed by <b>Shakibul Hasan</b> | CSE Student | {datetime.now().year}</div>", unsafe_allow_html=True)
