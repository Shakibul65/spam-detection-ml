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

# ১. রেসপন্সিভ পেজ সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম সিএসএস (UI Fix)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background: linear-gradient(90deg, #1e3c72, #2a5298); 
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .status-card { 
        background: white; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-left: 5px solid #1e3c72;
    }
    .footer { text-align: center; color: #666; padding: 20px; border-top: 1px solid #ddd; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন (নির্ভুল করার জন্য আরও ডাটা যোগ করা হয়েছে)
@st.cache_resource
def load_engine():
    data = {
        'text': [
            'Free money now', 'Hi, how are you?', 'Claim prize money', 'Meeting at 10', 
            'Win gift card', 'Call me soon', 'Congratulations you won cash', 'Project report',
            'Account locked login here', 'Your OTP is 1234', 'Double income today', 'Lunch today?',
            'Get 100% discount', 'Can we talk?', 'Urgent: Verify identity', 'File received',
            'Invest now for profit', 'Click here for reward', 'Help with homework', 'See you later'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    
    # Accuracy calculate for CK
    y_pred = model.predict(X)
    acc = accuracy_score(df['label'], y_pred)
    return cv, model, acc

cv, model, model_acc = load_engine()

# ৪. সাইডবার
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown(f"**Dev:** Shakibul Hasan")
    st.caption("CSE Student | Jamalpur, BD")
    st.markdown("---")
    menu = st.radio("Applications", ["📊 Dashboard", "🔍 Spam Detector", "🔗 URL Scanner", "📁 Bulk Analyzer", "💡 Insights"])
    st.markdown("---")
    st.success(f"System Accuracy: {model_acc*100:.1f}%")

# ৫. ড্যাশবোর্ড
if menu == "📊 Dashboard":
    st.title("🚀 Security Overview")
    cols = st.columns(4)
    cols[0].metric("Total Scanned", "4.2k", "+15%")
    cols[1].metric("Spam Blocked", "912", "+8%")
    cols[2].metric("Phishing Sites", "142", "+22%")
    cols[3].metric("Risk Level", "Low", "Stable")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Weekly Threat Analytics")
        st.area_chart(pd.DataFrame({'Threats': [10, 25, 15, 45, 30, 10, 5]}))
    with c2:
        st.subheader("Model Reliability")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=model_acc*100, gauge={'bar':{'color':"#1e3c72"}}))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

# ৬. স্প্যাম ডিটেক্টর
elif menu == "🔍 Spam Detector":
    st.title("🔍 Advanced Spam Guard")
    user_input = st.text_area("Analyze Text Content:", height=150, placeholder="Paste message here...")
    
    if st.button("Start AI Analysis 🚀"):
        if user_input:
            with st.spinner('Scanning...'):
                time.sleep(0.5)
                vect = cv.transform([user_input])
                res = model.predict(vect)[0]
                prob = model.predict_proba(vect)[0]
                
                st.markdown("<div class='status-card'>", unsafe_allow_html=True)
                if res == 'spam':
                    st.error(f"🚨 ALERT: SPAM DETECTED! ({prob[1]*100:.1f}% confidence)")
                else:
                    st.success(f"✅ SAFE CONTENT ({prob[0]*100:.1f}% confidence)")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Input required.")

# ৭. ইউআরএল স্ক্যানার (লজিক আরও একুরেট করা হয়েছে)
elif menu == "🔗 URL Scanner":
    st.title("🔗 Phishing Link Intelligence")
    url_input = st.text_input("Enter URL Path:", placeholder="http://secure-login-verify.com")
    
    if st.button("Check Link Safety ⚙️"):
        if url_input:
            # Accuracy updates for scoring
            score = 0
            if len(url_input) > 50: score += 30
            if any(x in url_input.lower() for x in ['login', 'verify', 'update', 'secure', 'bank', 'free']): score += 40
            if url_input.count('.') > 3: score += 30
            
            st.markdown(f"<div class='status-card'>Link Scanned. Risk Score: <b>{score}/100</b></div>", unsafe_allow_html=True)
            if score >= 50:
                st.error("🚨 HIGH RISK: This link shows phishing patterns!")
            else:
                st.success("✅ LOW RISK: Link appears to be safe.")
        else:
            st.warning("Please provide a URL.")

# ৮. বাল্ক এনালাইজার
elif menu == "📁 Bulk Analyzer":
    st.title("📁 Batch Processing")
    file = st.file_uploader("Upload CSV (text column needed)", type=["csv"])
    if file:
        df_csv = pd.read_csv(file)
        if 'text' in df_csv.columns:
            if st.button("Run Bulk Scan"):
                vect_bulk = cv.transform(df_csv['text'].astype(str))
                df_csv['Status'] = model.predict(vect_bulk)
                st.dataframe(df_csv, use_container_width=True)
                st.bar_chart(df_csv['Status'].value_counts())
        else:
            st.error("Column 'text' not found.")

# ৯. সিকিউরিটি ইনসাইটস (Syntax Error ফিক্স করা হয়েছে)
elif menu == "💡 Insights":
    st.title("💡 Security Intelligence")
    t1, t2 = st.tabs(["🛡️ Safety Guide", "📡 Threat Map"])
    with t1:
        st.markdown("""
        ### How to stay safe?
        - **Verify Domain:** Always check the spelling of the website address.
        - **2FA:** Enable Two-Factor Authentication for all accounts.
        - **Sense of Urgency:** Be careful of messages that demand immediate action.
        """)
        st.info("💡 **Pro Tip:** Never share your OTP with anyone over a call or message.")
    with t2:
        st.plotly_chart(px.pie(names=['Phishing', 'Spam', 'Malware'], values=[45, 35, 20], hole=0.3), use_container_width=True)

# ১০. ফুটার
st.markdown(f"<div class='footer'>Developed by <b>Shakibul Hasan</b> | CSE Student | {datetime.now().year}</div>", unsafe_allow_html=True)
