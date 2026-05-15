import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
import time

# ১. রেসপন্সিভ পেজ সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. অ্যাডভান্সড রেসপন্সিভ কাস্টম সিএসএস (Mobile-First Approach)
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .main { background-color: #f8f9fa; }
    
    /* রেসপন্সিভ মেট্রিক কার্ড */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    
    /* বাটন ডিজাইন */
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background: linear-gradient(90deg, #007bff, #00c6ff); 
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,123,255,0.3); }

    /* রেসপন্সিভ ইমেজ এবং কার্ড */
    .result-card { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #007bff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* ফুটার ডিজাইন (মোবাইলে হাইড হবে না) */
    .footer { 
        position: relative; margin-top: 50px; width: 100%; 
        text-align: center; color: #666; padding: 20px; 
        background: transparent; border-top: 1px solid #ddd; 
    }

    /* টেক্সট এরিয়া মোবাইল রেসপন্সিভনেস */
    @media (max-width: 768px) {
        .stTextArea textarea { height: 150px !important; }
        [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন ক্যাশ লোড
@st.cache_resource
def load_ai_engine():
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
    return cv, model, df

cv, model, base_df = load_ai_engine()

# ইউআরএল এনালাইসিস লজিক
def analyze_url(url):
    score = 0
    reasons = []
    if len(url) > 60: score += 30; reasons.append("Long URL")
    if any(x in url.lower() for x in ['login', 'verify', 'secure', 'bank', 'free']): score += 40; reasons.append("Keyword Match")
    if url.count('.') > 3: score += 30; reasons.append("Subdomain Stacking")
    return score, reasons

# ৪. সাইডবার (রেসপন্সিভ নেভিগেশন)
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown(f"**Developer:** Shakibul Hasan")
    st.caption("CSE Student | Freelancer")
    st.markdown("---")
    menu = st.radio("Applications", ["📊 Dashboard", "🔍 Spam Detector", "🔗 URL Scanner", "📁 Bulk Analyzer", "💡 Insights"])
    st.markdown("---")
    st.write(f"System Time: {datetime.now().strftime('%H:%M')}")

# ৫. ড্যাশবোর্ড পেজ
if menu == "📊 Dashboard":
    st.title("🚀 Security Overview")
    
    # রেসপন্সিভ কলাম
    m1, m2, m3, m4 = st.columns([1,1,1,1])
    m1.metric("Scanned", "3.1k", "+18%")
    m2.metric("Blocked", "845", "+7%")
    m3.metric("Sites", "142", "+22%")
    m4.metric("Risk", "Low", "-3%")
    
    st.markdown("---")
    c1, c2 = st.columns([1, 1], gap="medium")
    with c1:
        st.subheader("Attack Patterns")
        st.area_chart(pd.DataFrame({'Threats': [10, 25, 15, 45, 30, 10, 5]}))
    with c2:
        st.subheader("System Accuracy")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=98.5, gauge={'axis':{'range':[0,100]}, 'bar':{'color':"#007bff"}}))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

# ৬. স্প্যাম ডিটেক্টর
elif menu == "🔍 Spam Detector":
    st.title("🔍 Spam Guard")
    user_input = st.text_area("Input message for analysis:", height=200)
    
    if st.button("Start Analysis 🚀"):
        if user_input:
            with st.spinner('Checking...'):
                time.sleep(0.5)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)[0]
                prob = model.predict_proba(vect)[0]
                
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                if prediction == 'spam':
                    st.error(f"🚨 SPAM DETECTED! (Confidence: {prob[1]*100:.1f}%)")
                else:
                    st.success(f"✅ SAFE MESSAGE (Confidence: {prob[0]*100:.1f}%)")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter text.")

# ৭. ইউআরএল স্ক্যানার
elif menu == "🔗 URL Scanner":
    st.title("🔗 URL Intelligence")
    url_input = st.text_input("Enter URL:")
    if st.button("Check Link ⚙️"):
        if url_input:
            score, reasons = analyze_url(url_input)
            col_u1, col_u2 = st.columns([1, 1])
            with col_u1:
                if score >= 50:
                    st.error(f"🚨 RISK DETECTED! (Score: {score}/100)")
                    for r in reasons: st.write(f"- {r}")
                else:
                    st.success(f"✅ URL SAFE (Score: {score}/100)")
            with col_u2:
                fig_risk = px.pie(values=[score, 100-score], names=['Risk', 'Safe'], hole=0.6, color_discrete_sequence=['red', 'green'])
                fig_risk.update_layout(height=250, showlegend=False)
                st.plotly_chart(fig_risk, use_container_width=True)

# ৮. বাল্ক এনালাইজার
elif menu == "📁 Bulk Analyzer":
    st.title("📁 CSV Bulk Scan")
    uploaded_file = st.file_uploader("Upload CSV (text column required)", type=["csv"])
    if uploaded_file:
        df_csv = pd.read_csv(uploaded_file)
        if 'text' in df_csv.columns:
            if st.button("Process CSV ⚡"):
                with st.spinner('Scanning...'):
                    vect_bulk = cv.transform(df_csv['text'].astype(str))
                    df_csv['Status'] = model.predict(vect_bulk)
                    st.dataframe(df_csv, use_container_width=True)
                    st.bar_chart(df_csv['Status'].value_counts())
        else:
            st.error("Column 'text' missing.")

# ৯. সিকিউরিটি ইনসাইটস
elif menu == "💡 Insights":
    st.title("💡 Safety Center")
    t1, t2 = st.tabs(["🛡️ Safety Guide", "📡 Threat Trends"])
    with t1:
        st.markdown("""
        - **MFA:** Always use multi-factor authentication.
        - **Domain:** Verify sender domain name.
        - **Urgency:** Avoid messages with fake threats.
        """)
        st.image("https://img.freepik.com/free-vector/phishing-concept-flat-design_23-2148529367.jpg", use_container_width=True)
    with t2:
        st.plotly_chart(px.pie(names=['Email', 'SMS', 'Voice'], values=[50, 30, 20], hole=0.3), use_container_width=True)

# ১০. রেসপন্সিভ ফুটার
st.markdown(f"""
    <div class="footer">
        <p>Developed by <b>Shakibul Hasan</b> | CSE Student | {datetime.now().year}</p>
    </div>
    """, unsafe_allow_html=True)
