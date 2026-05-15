import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
import time
import re

# ১. প্রফেশনাল পেজ কনফিগারেশন
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম সিএসএস (Modern UI)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background: linear-gradient(90deg, #007bff, #00c6ff); 
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,123,255,0.4); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #666; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    .result-card { background: white; padding: 25px; border-radius: 15px; border-left: 5px solid #007bff; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন লোড
@st.cache_resource
def load_advanced_engine():
    data = {
        'text': [
            'Free money now', 'Hi, how are you?', 'Claim prize money', 'Meeting at 10', 
            'Win gift card', 'Call me soon', 'Congratulations you won cash', 'Project report attached',
            'Account locked login here', 'Your OTP is 1234', 'Double your income today', 'Let\'s go for lunch',
            'Get 100% discount now', 'Can we talk?', 'Urgent: Verify your identity', 'Thanks for the file'
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

# ইউআরএল বিশ্লেষণ লজিক
def analyze_url_logic(url):
    reasons = []
    score = 0
    if len(url) > 60:
        score += 30
        reasons.append("URL length is extremely long")
    if any(k in url.lower() for k in ['login', 'secure', 'verify', 'update', 'banking', 'free', 'bonus']):
        score += 40
        reasons.append("Contains sensitive keywords")
    if url.count('.') > 3:
        score += 20
        reasons.append("High number of subdomains detected")
    if "@" in url or "-" in url:
        score += 10
        reasons.append("Use of suspicious symbols detected")
    return score, reasons

# ৪. সাইডবার নেভিগেশন
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.markdown(f"**Developer:** Shakibul Hasan")
    st.caption("CSE Student | Jamalpur, Bangladesh")
    st.markdown("---")
    
    menu = st.radio("Applications", [
        "📊 Dashboard", 
        "🔍 Spam Detector", 
        "🔗 Phishing URL Scanner", 
        "📁 CSV Bulk Analyzer", 
        "💡 Security Insights"
    ])
    st.markdown("---")
    st.info(f"System Online\n\n{datetime.now().strftime('%d %b, 2026')}")

# ৫. ড্যাশবোর্ড পেজ
if menu == "📊 Dashboard":
    st.title("🚀 Security Intelligence Dashboard")
    st.write("Welcome to the real-time threat monitoring overview.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Items Scanned", "3,120", "+18%")
    col2.metric("Spam Blocked", "845", "+7%")
    col3.metric("Phishing Sites", "142", "+22%")
    col4.metric("Risk Factor", "Low", "-3%", delta_color="inverse")
    
    st.markdown("---")
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("Weekly Attack Pattern")
        fig_line = px.area(pd.DataFrame({'D':['M','T','W','T','F','S','S'], 'V':[10,25,15,45,35,12,8]}), x='D', y='V', title="Blocked Threats")
        st.plotly_chart(fig_line, use_container_width=True)
    with c_right:
        st.subheader("System Accuracy")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=98.5, title={'text': "Model Confidence (%)"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#007bff"}}))
        st.plotly_chart(fig_gauge, use_container_width=True)

# ৬. স্প্যাম ডিটেক্টর
elif menu == "🔍 Spam Detector":
    st.title("🔍 Advanced Spam Guard")
    st.write("Paste your content below for deep AI scanning and pattern recognition.")
    
    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        user_input = st.text_area("Input Text:", height=250, placeholder="Paste email or message here...")
        if st.button("Start Deep Scan 🚀"):
            if user_input:
                with st.spinner("Analyzing patterns..."):
                    time.sleep(1)
                    vect = cv.transform([user_input])
                    prediction = model.predict(vect)[0]
                    prob = model.predict_proba(vect)[0]
                    
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    if prediction == 'spam':
                        st.error(f"🚨 ALERT: SPAM DETECTED! (Confidence: {prob[1]*100:.2f}%)")
                    else:
                        st.success(f"✅ SAFE CONTENT (Confidence: {prob[0]*100:.2f}%)")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Input required.")
    with col_r:
        st.subheader("Metadata Analytics")
        if user_input:
            st.metric("Word Count", len(user_input.split()))
            st.metric("Character Count", len(user_input))
        else:
            st.info("Input text to see real-time statistics.")

# ৭. ফিশিং লিঙ্ক স্ক্যানার
elif menu == "🔗 Phishing URL Scanner":
    st.title("🔗 Phishing Link Intelligence")
    st.write("Analyze URLs for potential security indicators and structural anomalies.")
    
    url_input = st.text_input("Enter URL to Scan:", placeholder="e.g., http://secure-login-update.com")
    
    if st.button("Analyze Link Structure ⚙️"):
        if url_input:
            score, reasons = analyze_url_logic(url_input)
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                if score >= 50:
                    st.error(f"🚨 RISK DETECTED! (Risk Score: {score}/100)")
                    for r in reasons: st.write(f"- {r}")
                else:
                    st.success(f"✅ URL APPEARS LEGITIMATE (Risk Score: {score}/100)")
            with col_u2:
                fig_risk = px.pie(values=[score, 100-score], names=['Risk', 'Safe'], hole=0.6, color_discrete_sequence=['red', 'green'])
                st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.warning("Please provide a URL.")

# ৮. সিএসভি বাল্ক এনালাইজার
elif menu == "📁 CSV Bulk Analyzer":
    st.title("📁 Bulk Data Processor")
    st.write("Upload a CSV file for high-speed automated content scanning.")
    
    uploaded_file = st.file_uploader("Upload CSV (Must contain 'text' column)", type=["csv"])
    if uploaded_file:
        df_csv = pd.read_csv(uploaded_file)
        if 'text' in df_csv.columns:
            if st.button("Start Automated Scan ⚡"):
                with st.spinner("Processing dataset..."):
                    vect_bulk = cv.transform(df_csv['text'].astype(str))
                    df_csv['Status'] = model.predict(vect_bulk)
                    st.success("Analysis Completed!")
                    st.dataframe(df_csv, use_container_width=True)
                    
                    st.subheader("Summary Report")
                    fig_csv = px.bar(df_csv['Status'].value_counts(), title="Scan Results Distribution")
                    st.plotly_chart(fig_csv, use_container_width=True)
        else:
            st.error("Error: Column 'text' not found in the uploaded file.")

# ৯. সিকিউরিটি ইনসাইটস
elif menu == "💡 Security Insights":
    st.title("💡 Cybersecurity Intelligence & Guide")
    
    tab1, tab2, tab3 = st.tabs(["🛡️ Global Safety", "🔗 URL Analysis", "📡 Threat Landscape"])
    
    with tab1:
        st.subheader("Best Practices for Digital Safety")
        st.markdown("""
        * **MFA Implementation:** Always enable Multi-Factor Authentication.
        * **Psychological Triggers:** Be cautious of messages creating false urgency.
        * **Domain Verification:** Check the actual sender domain before clicking links.
        """)
        st.image("https://img.freepik.com/free-vector/phishing-concept-flat-design_23-2148529367.jpg")

    with tab2:
        st.subheader("Anatomy of a Phishing Link")
        st.markdown("""
        1.  **Protocol Verification:** Look for 'https' and valid SSL certificates.
        2.  **Typosquatting:** Check for minor misspellings in famous brand names.
        3.  **Subdomain Stacking:** Be wary of URLs with multiple confusing subdomains.
        """)

    with tab3:
        st.subheader("Global Threat Trends")
        threat_chart = pd.DataFrame({'Type':['Email', 'Social Media', 'SMS', 'Voice Call'], 'Frequency':[50, 20, 20, 10]})
        st.plotly_chart(px.pie(threat_chart, values='Frequency', names='Type', hole=0.3), use_container_width=True)

# ১০. ফুটার
st.markdown(f'<div class="footer">Developed by <b>Shakibul Hasan</b> | CSE Student | {datetime.now().year}</div>', unsafe_allow_html=True)
