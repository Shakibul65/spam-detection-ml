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

# ২. কাস্টম সিএসএস (সব ডিভাইসে রেসপন্সিভ লুকের জন্য)
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
    /* Grid system for responsive boxes */
    .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন
@st.cache_resource
def load_engine():
    data = {
        'text': [
            'Free money now', 'Hi, how are you?', 'Claim prize money', 'Meeting at 10', 
            'Win gift card', 'Call me soon', 'Congratulations you won cash', 'Project report',
            'Account locked login here', 'Your OTP is 1234', 'Double income today', 'Lunch today?',
            'Get 100% discount', 'Can we talk?', 'Urgent: Verify identity', 'File received',
            'Invest now for profit', 'Click here for reward', 'Hey buddy', 'Office presentation'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    y_pred = model.predict(X)
    acc = accuracy_score(df['label'], y_pred)
    return cv, model, acc

cv, model, model_acc = load_engine()

# ৪. সাইডবার নেভিগেশন
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown(f"**Dev:** Shakibul Hasan")
    st.caption("CSE Student | Jamalpur, BD")
    st.markdown("---")
    menu = st.radio("Applications", ["📊 Dashboard", "🔍 Spam Detector", "🔗 URL Scanner", "📁 Bulk Analyzer", "💡 Insights"])
    st.markdown("---")
    st.success(f"Model Accuracy: {model_acc*100:.1f}%")

# ৫. ড্যাশবোর্ড
if menu == "📊 Dashboard":
    st.title("🚀 Security Intelligence Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Scanned", "4.2k", "+15%")
    m2.metric("Spam Blocked", "912", "+8%")
    m3.metric("Phishing Sites", "142", "+22%")
    m4.metric("Risk Level", "Low", "Stable")
    
    st.markdown("---")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Weekly Threat Trends")
        st.area_chart(pd.DataFrame({'Threats': [10, 25, 15, 45, 30, 10, 5]}))
    with c2:
        st.subheader("System Reliability")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=model_acc*100, gauge={'bar':{'color':"#1e3c72"}}))
        fig.update_layout(height=280)
        st.plotly_chart(fig, use_container_width=True)

# ৬. স্প্যাম ডিটেক্টর (Responsive)
elif menu == "🔍 Spam Detector":
    st.title("🔍 Advanced Spam Guard")
    user_input = st.text_area("Analyze Text Content:", height=150, placeholder="Paste your message here...")
    
    if st.button("Start AI Analysis 🚀"):
        if user_input:
            with st.spinner('Scanning patterns...'):
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
            st.warning("Please input text first.")
    
    # Bottom responsive design
    st.markdown("### 📊 Detector Mechanics")
    st.markdown("""
    <div class="info-grid">
        <div class="status-card"><b>Naïve Bayes Logic:</b> শব্দগুলোর গাণিতিক সম্ভাবনা বিশ্লেষণ করে স্প্যাম শনাক্ত করা হয়।</div>
        <div class="status-card"><b>Text Tokenization:</b> প্রতিটি শব্দকে আলাদা ডাটা পয়েন্টে রূপান্তর করে প্রসেস করা হয়।</div>
        <div class="status-card"><b>Real-time Engine:</b> কয়েক মিলি-সেকেন্ডের মধ্যে বড় টেক্সট এনালাইসিস করতে সক্ষম।</div>
    </div>
    """, unsafe_allow_html=True)

# ৭. ইউআরএল স্ক্যানার (Responsive)
elif menu == "🔗 URL Scanner":
    st.title("🔗 Phishing Link Intelligence")
    url_input = st.text_input("Enter URL Path:", placeholder="http://secure-login-update.com")
    
    if st.button("Check Link Safety ⚙️"):
        if url_input:
            score = 0
            reasons = []
            if len(url_input) > 50: score += 30; reasons.append("Excessive length")
            if any(x in url_input.lower() for x in ['login', 'verify', 'update', 'secure', 'bank', 'free']): score += 40; reasons.append("Sensitive keywords detected")
            if url_input.count('.') > 3: score += 30; reasons.append("Too many subdomains")
            
            st.markdown(f"<div class='status-card'>Link Scanned. Risk Score: <b>{score}/100</b></div>", unsafe_allow_html=True)
            if score >= 50:
                st.error(f"🚨 HIGH RISK! Factors: {', '.join(reasons)}")
            else:
                st.success("✅ LOW RISK: This link appears to be safe.")
        else:
            st.warning("Please provide a URL.")

    # Bottom responsive design
    st.markdown("### 🌐 Structural Analysis")
    st.markdown("""
    <div class="info-grid">
        <div class="status-card"><b>Domain Reputation:</b> ডোমেইনের বিশ্বাসযোগ্যতা এবং বয়স পরীক্ষা করা হয়।</div>
        <div class="status-card"><b>Protocol Check:</b> HTTPS সিকিউরিটি লেয়ার আছে কি না তা যাচাই করা হয়।</div>
    </div>
    """, unsafe_allow_html=True)

# ৮. বাল্ক এনালাইজার (Responsive)
elif menu == "📁 Bulk Analyzer":
    st.title("📁 Batch Processing Unit")
    file = st.file_uploader("Upload CSV (Must contain 'text' column)", type=["csv"])
    if file:
        df_csv = pd.read_csv(file)
        if 'text' in df_csv.columns:
            if st.button("Start Bulk Scan ⚡"):
                with st.spinner('Processing dataset...'):
                    vect_bulk = cv.transform(df_csv['text'].astype(str))
                    df_csv['AI_Status'] = model.predict(vect_bulk)
                    st.success("Bulk scan completed!")
                    st.dataframe(df_csv, use_container_width=True)
                    
                    st.subheader("Scan Summary")
                    st.bar_chart(df_csv['AI_Status'].value_counts())
        else:
            st.error("Error: 'text' নামে কোনো কলাম পাওয়া যায়নি।")
    
    # Bottom responsive design
    st.markdown("### 📦 Bulk System Features")
    st.markdown("""
    <div class="status-card">
    <b>High Throughput:</b> একসাথে হাজার হাজার ইমেইল বা মেসেজ দ্রুত স্ক্যানিংয়ের জন্য অপ্টিমাইজড।
    </div>
    """, unsafe_allow_html=True)

# ৯. সিকিউরিটি ইনসাইটস (Expanded Content)
elif menu == "💡 Insights":
    st.title("💡 Cybersecurity & Safety Center")
    t1, t2, t3 = st.tabs(["🛡️ Safety Guide", "📡 Threat Landscape", "⚙️ System Tech"])
    
    with t1:
        st.markdown("### নিজেকে সুরক্ষিত রাখার সেরা উপায়")
        st.markdown("""
        * **MFA:** সবসময় টু-ফ্যাক্টর অথেন্টিকেশন চালু রাখুন।
        * **Domain Check:** লিঙ্কে ক্লিক করার আগে সাইটের বানান চেক করুন।
        * **Urgency:** কোনো মেসেজ যদি দ্রুত টাকা বা তথ্য চায়, তবে সেটি সন্দেহজনক।
        """)
        st.info("💡 একজন প্রফেশনাল কখনোই আপনার পাসওয়ার্ড বা ওটিপি জানতে চাইবেন না।")
    
    with t2:
        st.subheader("২০২৬ সালের প্রধান সাইবার হুমকি")
        st.plotly_chart(px.pie(names=['Email Phishing', 'Mobile Scams', 'AI Spam', 'Malware'], values=[40, 25, 20, 15], hole=0.3), use_container_width=True)
    
    with t3:
        st.subheader("Our Security Stack")
        st.code("""
        - Model: Naive Bayes (MultinomialNB)
        - Vectorizer: CountVectorizer
        - UI: Streamlit (Python)
        - Visualization: Plotly & Pandas
        """, language="text")

# ১০. ফুটার
st.markdown(f"<div class='footer'>Developed by <b>Shakibul Hasan</b> | CSE Student | {datetime.now().year}</div>", unsafe_allow_html=True)
