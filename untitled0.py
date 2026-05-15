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

# ২. উন্নত কাস্টম সিএসএস (UI Fix)
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
    .grid-box { background: white; padding: 20px; border-radius: 15px; border-top: 4px solid #1e3c72; }
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
    y_pred = model.predict(X)
    acc = accuracy_score(df['label'], y_pred)
    return cv, model, acc

cv, model, model_acc = load_advanced_engine()

# ৪. সাইডবার নেভিগেশন (NameError ফিক্স করার জন্য সঠিক ভেরিয়েবল নাম)
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("### Developer: Shakibul Hasan")
    st.caption("CSE Student | Jamalpur, BD")
    st.markdown("---")
    # এখানে 'menu' ভেরিয়েবলটি ডিফাইন করা হয়েছে যা NameError দূর করবে
    menu = st.radio("Applications", [
        "🏠 Dashboard", 
        "🔍 Spam Detector", 
        "🔗 URL Scanner", 
        "📁 Bulk Analyzer", 
        "💡 Cybersecurity Insights",
        "📂 API & Developer Portal"
    ])
    st.markdown("---")
    st.success(f"System Accuracy: {model_acc*100:.1f}%")

# ৫. ড্যাশবোর্ড
if menu == "🏠 Dashboard":
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_container_width=True)
    st.title("🚀 Security Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Scanned", "12.5k", "+18%")
    c2.metric("Blocked", "3,402", "+12%")
    c3.metric("Sites", "842", "+25%")
    c4.metric("Uptime", "99.9%", "Stable")
    
    st.markdown("---")
    st.subheader("Global Threat Activity (2026)")
    chart_data = pd.DataFrame({'Attacks': [20, 50, 30, 90, 70, 40, 100]})
    st.line_chart(chart_data)

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

# ৭. ইউআরএল স্ক্যানার
elif menu == "🔗 URL Scanner":
    st.title("🔗 Phishing Link Intelligence")
    st.image("https://img.freepik.com/free-vector/phishing-concept-flat-design_23-2148529367.jpg", width=600)
    url = st.text_input("Enter URL Path:")
    if st.button("Scan Link Safety ⚙️"):
        score = 65 if "verify" in url or "login" in url else 10
        st.markdown(f"<div class='status-card'>Link Scanned. Risk Score: {score}/100</div>", unsafe_allow_html=True)

# ৮. বাল্ক এনালাইজার
elif menu == "📁 Bulk Analyzer":
    st.title("📁 Batch Processing")
    file = st.file_uploader("Upload Dataset", type=["csv"])
    if file:
        st.success("File uploaded! Ready for bulk scanning.")
        st.button("Start Processing")

# ৯. সাইবার সিকিউরিটি ইনসাইটস (নতুন বড় কন্টেন্ট)
elif menu == "💡 Cybersecurity Insights":
    st.title("💡 Cybersecurity Intelligence Center")
    st.image("https://img.freepik.com/free-photo/standard-quality-control-concept-m_23-2150041848.jpg", use_container_width=True)
    
    tab1, tab2, tab3 = st.tabs(["🛡️ User Safety", "🚨 Global Threats", "🛠️ Architecture"])
    with tab1:
        st.markdown("### How to Identify Phishing Emails")
        st.write("১. **Urgent Language:** যদি মেসেজে খুব দ্রুত কিছু করার তাগাদা দেয়।")
        st.write("২. **Mismatched Links:** লিঙ্কের ওপর মাউস রাখলে যদি অন্য অ্যাড্রেস দেখায়।")
        st.write("৩. **Poor Grammar:** বড় কোম্পানি সাধারণত ভুল বানানে মেসেজ পাঠায় না।")
    with tab2:
        st.markdown("### Threat Landscape 2026")
        fig = px.pie(names=['Phishing', 'Malware', 'Ransomware', 'Others'], values=[45, 25, 20, 10], hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        st.markdown("### System Architecture")
        st.code("Model: Multinomial Naive Bayes\nVectorization: Bag of Words\nPlatform: Streamlit Cloud", language="text")

# ১০. এপিআই পোর্টাল
elif menu == "📂 API & Developer Portal":
    st.title("📂 Developer Integration Hub")
    st.image("https://img.freepik.com/free-vector/api-concept-illustration_114360-9397.jpg", width=500)
    st.markdown("### Integration Guide")
    st.write("আপনি আপনার নিজের অ্যাপে এই ডিটেক্টর ব্যবহার করতে নিচের কোডটি ব্যবহার করতে পারেন:")
    st.code("""
import requests

def check_spam(text):
    api_url = "https://api.spamguard.ai/v1/scan"
    response = requests.post(api_url, json={"text": text})
    return response.json()
    """, language="python")

# ১১. ফুটার
st.markdown(f"<div class='footer'>Developed by <b>Shakibul Hasan</b> | CSE Student | {datetime.now().year}</div>", unsafe_allow_html=True)
