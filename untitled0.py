import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="SpamGuard AI", page_icon="🛡️", layout="wide")

# ২. মডার্ন ও সুদিং ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #e2e8f0; }
    
    /* সাইডবার */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }

    /* প্রিমিয়াম ফ্লো কার্ড (নিচের আইকনগুলো) */
    .premium-flow-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(99, 102, 241, 0.1);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        transition: 0.4s;
    }
    .premium-flow-card:hover {
        background: rgba(99, 102, 241, 0.05);
        border-color: #6366f1;
        transform: translateY(-5px);
    }

    /* এনিমেটেড ফ্লোটিং আইকন */
    .icon-box {
        font-size: 35px;
        margin-bottom: 10px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    /* রেজাল্ট কার্ড - লেখাগুলো এখন আরও মার্জিত */
    .result-text {
        font-size: 22px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    .confidence-text {
        font-size: 14px;
        opacity: 0.8;
        margin-top: 5px;
    }
    .ham-box {
        background: rgba(34, 197, 94, 0.05);
        border: 1px solid #22c55e;
        padding: 20px; border-radius: 15px; text-align: center;
    }
    .spam-box {
        background: rgba(239, 68, 68, 0.05);
        border: 1px solid #ef4444;
        padding: 20px; border-radius: 15px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. ৫০০০+ ডেটাসেট ও মডেল লোড
@st.cache_resource
def get_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model, len(df)

cv, model, data_size = get_model()

# ৪. সাইডবার ডিটেইলস
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #6366f1;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.info("**Shakibul Hasan**\n\nCSE Student | Freelancer")
    st.markdown("---")
    st.caption(f"Dataset: {data_size} Messages")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>AI Message Analyzer</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
with col2:
    st.markdown('<div style="background: rgba(30, 41, 59, 0.6); padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">', unsafe_allow_html=True)
    user_input = st.text_area("আপনার মেসেজটি এখানে লিখুন:", height=150, placeholder="Paste message here...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI প্রসেসিং চলছে...'):
                time.sleep(1)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                conf = max(prob[0]) * 100

            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                st.markdown(f'''
                    <div class="spam-box">
                        <div class="result-text" style="color: #ef4444;">🚨 এটি একটি স্প্যাম মেসেজ</div>
                        <div class="confidence-text">নিশ্চয়তা: {conf:.2f}%</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.snow()
            else:
                st.markdown(f'''
                    <div class="ham-box">
                        <div class="result-text" style="color: #22c55e;">✅ এটি একটি নিরাপদ মেসেজ</div>
                        <div class="confidence-text">নিশ্চয়তা: {conf:.2f}%</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.balloons()
        else:
            st.warning("দয়া করে কিছু লিখুন!")
    st.markdown('</div>', unsafe_allow_html=True)

# ৬. নিচের আইকন কার্ডস (Floating)
st.markdown("<br>", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown('<div class="premium-flow-card"><div class="icon-box">🛡️</div><h4 style="color: #6366f1;">Privacy</h4><p style="font-size: 13px; opacity: 0.7;">ডেটা সম্পূর্ণ নিরাপদ</p></div>', unsafe_allow_html=True)
with f2:
    st.markdown('<div class="premium-flow-card"><div class="icon-box">⚡</div><h4 style="color: #6366f1;">Fast</h4><p style="font-size: 13px; opacity: 0.7;">মিলি-সেকেন্ডে বিশ্লেষণ</p></div>', unsafe_allow_html=True)
with f3:
    st.markdown('<div class="premium-flow-card"><div class="icon-box">🎯</div><h4 style="color: #6366f1;">Accuracy</h4><p style="font-size: 13px; opacity: 0.7;">হাই-প্রিসিশন SVM</p></div>', unsafe_allow_html=True)

st.markdown("<br><center style='font-size: 12px; opacity: 0.5;'>Developed by Shakibul Hasan | 2026</center>", unsafe_allow_html=True)
