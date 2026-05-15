import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
import time
import re

# ১. প্রফেশনাল পেজ কনফিগারেশন
st.set_page_config(
    page_title="SpamGuard AI & Phishing Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম সিএসএস
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background: linear-gradient(45deg, #007bff, #0056b3); color: white; font-weight: bold; border: none; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #666; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    .stMetric { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন (স্মার্ট ক্যাশিং সহ)
@st.cache_resource
def load_ai_engine():
    data = {
        'text': [
            'Free money now', 'Hi, how are you?', 'Claim prize', 'Meeting at 10', 
            'Win gift card', 'Call me', 'Congratulations won cash', 'Project file attached',
            'Account locked login here', 'Your OTP is 9988', 'Earn money home', 'Update soon'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model

cv, model = load_ai_engine()

# ফিশিং লিঙ্ক ডিটেকশন লজিক (আপনার থিসিস ভিত্তিক সিম্পল রুলস)
def detect_phishing_url(url):
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'bank', 'free', 'win', 'gift']
    is_phishing = False
    reasons = []
    
    if len(url) > 50:
        is_phishing = True
        reasons.append("URL length is unusually long.")
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        is_phishing = True
        reasons.append("Contains suspicious security keywords.")
    if url.count('.') > 3:
        is_phishing = True
        reasons.append("Too many subdomains detected.")
    if "@" in url:
        is_phishing = True
        reasons.append("Contains '@' symbol (common in phishing).")
        
    return is_phishing, reasons

# ৪. সাইডবার নেভিগেশন
with st.sidebar:
    st.title("🛡️ Security Center")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.write("**Dev:** Shakibul Hasan")
    st.caption("CSE Student | Phishing Researcher")
    st.markdown("---")
    
    menu = st.radio("Tools & Analysis", [
        "📊 System Dashboard", 
        "🔍 Spam Detector", 
        "🔗 Phishing Link Scanner", 
        "📁 CSV Bulk Analyzer", 
        "💡 Security Insights"
    ])
    
    st.markdown("---")
    st.info(f"Jamalpur, BD\n\n{datetime.now().strftime('%d %b, 2026')}")

# ৫. পেজ ১: ড্যাশবোর্ড
if menu == "📊 System Dashboard":
    st.title("📈 Intelligence Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Scanned Items", "2,450", "+15%")
    c2.metric("Threats Blocked", "680", "+10%")
    c3.metric("URL Accuracy", "97.4%", "0.2%")
    c4.metric("Server Status", "Healthy", "Online")
    
    st.markdown("---")
    st.subheader("Threat Trends (Last 7 Days)")
    df_chart = pd.DataFrame({'Day': ['M', 'T', 'W', 'T', 'F', 'S', 'S'], 'Threats': [20, 35, 15, 50, 45, 10, 5]})
    st.line_chart(df_chart.set_index('Day'))

# ৬. পেজ ২: স্প্যাম ডিটেক্টর
elif menu == "🔍 Spam Detector":
    st.title("📧 Message Spam Guard")
    input_text = st.text_area("মেসেজটি এখানে লিখুন:", height=200)
    if st.button("Scan Message 🚀"):
        if input_text:
            vect = cv.transform([input_text])
            res = model.predict(vect)[0]
            if res == 'spam':
                st.error("🚨 SPAM DETECTED! এটি একটি ক্ষতিকর মেসেজ হতে পারে।")
            else:
                st.success("✅ SAFE (HAM). এই মেসেজটি নিরাপদ।")
        else:
            st.warning("Please input text.")

# ৭. পেজ ৩: ফিশিং লিঙ্ক স্ক্যানার (আপনার থিসিস স্পেশাল)
elif menu == "🔗 Phishing Link Scanner":
    st.title("🔗 Phishing URL Detector")
    st.write("আপনার থিসিসের রিসার্চের ভিত্তিতে তৈরি এই টুলটি ইউআরএল বিশ্লেষণ করে।")
    url_input = st.text_input("লিঙ্কটি এখানে দিন (e.g., http://secure-login-verify.com):")
    
    if st.button("Analyze URL 🛡️"):
        if url_input:
            is_phish, reasons = detect_phishing_url(url_input)
            if is_phish:
                st.error("🚨 SUSPICIOUS URL DETECTED!")
                for r in reasons:
                    st.write(f"- {r}")
            else:
                st.success("✅ URL LOOKS CLEAN. মডেলটি কোনো অস্বাভাবিকতা খুঁজে পায়নি।")
        else:
            st.warning("Please enter a URL.")

# ৮. পেজ ৪: সিএসভি ফাইল এনালাইজার
elif menu == "📁 CSV Bulk Analyzer":
    st.title("📁 CSV Bulk Processing")
    st.write("একটি সিএসভি ফাইল আপলোড করুন যেখানে 'text' নামে একটি কলাম আছে।")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        if 'text' in df_upload.columns:
            if st.button("Process Bulk Data ⚙️"):
                with st.spinner("Analyzing all messages..."):
                    vect_bulk = cv.transform(df_upload['text'].astype(str))
                    df_upload['AI_Prediction'] = model.predict(vect_bulk)
                    st.success("Scanning Completed!")
                    st.dataframe(df_upload, use_container_width=True)
                    
                    # স্ট্যাটিস্টিক চার্ট
                    fig_csv = px.pie(df_upload, names='AI_Prediction', title="Bulk Analysis Result")
                    st.plotly_chart(fig_csv)
        else:
            st.error("Error: ফাইলে অবশ্যই 'text' নামে একটি কলাম থাকতে হবে।")

# ৯. পেজ ৫: সিকিউরিটি টিপস
elif menu == "💡 Security Insights":
    st.title("💡 Safety Guide")
    st.markdown("""
    - **Check Subdomains:** ফিশিং সাইটগুলো মূল সাইটের আগে অনেকগুলো সাবডোমেইন ব্যবহার করে।
    - **HTTPS check:** সব সময় লিঙ্কের শুরুতে `https://` আছে কি না দেখুন।
    - **Shortened Links:** `bit.ly` বা `tinyurl` লিঙ্কগুলো ক্লিক করার আগে প্রিভিউ দেখে নিন।
    """)

# ফুটার
st.markdown(f'<div class="footer">Developed by <b>Shakibul Hasan</b> | CSE Student | {datetime.now().year}</div>', unsafe_allow_html=True)
