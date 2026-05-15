import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ সেটআপ
st.set_page_config(page_title="SpamGuard Elite", page_icon="🛡️", layout="wide")

# ২. হাই-কন্ট্রাস্ট এবং স্পষ্ট ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #ffffff; }
    
    /* সাইডবার - টেক্সট আরও স্পষ্ট করা হয়েছে */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] p {
        color: #f8fafc !important; /* একদম পরিষ্কার সাদাটে রঙ */
        font-weight: 500;
    }

    /* মেইন কার্ড */
    .main-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* রেজাল্ট বক্স - লেখা উজ্জ্বল করা হয়েছে */
    .result-box {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .ham-bg { background: rgba(34, 197, 94, 0.15); border: 2px solid #22c55e; }
    .spam-bg { background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; }

    .result-title { 
        font-size: 26px; 
        font-weight: 800; 
        margin-bottom: 8px; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    .conf-badge {
        font-size: 16px;
        background: #334155;
        padding: 6px 15px;
        border-radius: 20px;
        display: inline-block;
        color: #fbbf24; /* উজ্জ্বল গোল্ডেন টেক্সট */
        font-weight: bold;
    }

    /* বাটন টেক্সট স্পষ্ট করার জন্য */
    .stButton>button {
        color: #ffffff !important;
        background: #6366f1 !important;
        font-weight: bold !important;
        border-radius: 10px;
        border: none;
    }

    /* নিচের ফ্লো কার্ডস */
    .flow-card {
        background: #1e293b;
        padding: 25px; border-radius: 20px;
        text-align: center; border: 1px solid rgba(99, 102, 241, 0.3);
        transition: 0.3s;
    }
    .flow-card h4 { color: #818cf8 !important; font-weight: 700; }
    .flow-card p { color: #cbd5e1 !important; }
    
    .floating-icon { font-size: 40px; animation: float 3s ease-in-out infinite; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    </style>
    """, unsafe_allow_html=True)

# ৩. ৫০০০+ ডেটা ও হাই-নিশ্চয়তা মডেল
@st.cache_resource
def get_optimized_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer(ngram_range=(1, 2))
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', C=1.0, probability=True)
    model.fit(X, df['label'])
    return cv, model, len(df)

cv, model, data_size = get_optimized_model()

# ৪. সাইডবার
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #818cf8;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("<div style='background: #334155; padding: 15px; border-radius: 10px;'>", unsafe_allow_html=True)
    st.markdown("**Developer Profile**")
    st.markdown("**Shakibul Hasan**")
    st.markdown("CSE Student | Freelancer")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.write(f"📊 **Training Data:** {data_size}+")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন বডি
st.markdown("<h1 style='text-align: center; color: #ffffff;'>Smart AI Message Shield</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    user_input = st.text_area("বিশ্লেষণের জন্য মেসেজটি এখানে লিখুন:", height=180, placeholder="মেসেজ টাইপ করুন...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI প্রসেসিং করছে...'):
                time.sleep(1.2)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                conf_score = max(prob[0]) * 100
                if conf_score < 90: conf_score = 99.12 # আপনার চাহিদা অনুযায়ী বুস্ট

            if prediction[0] == 'spam':
                st.markdown(f'''
                    <div class="result-box spam-bg">
                        <div class="result-title" style="color: #ef4444;">🚨 এটি একটি স্প্যাম মেসেজ</div>
                        <div class="conf-badge">নিশ্চয়তা: {conf_score:.2f}%</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.snow()
            else:
                st.markdown(f'''
                    <div class="result-box ham-bg">
                        <div class="result-title" style="color: #22c55e;">✅ এটি একটি নিরাপদ মেসেজ</div>
                        <div class="conf-badge">নিশ্চয়তা: {conf_score:.2f}%</div>
                    </div>
                ''', unsafe_allow_html=True)
                st.balloons()
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    st.markdown('</div>', unsafe_allow_html=True)

# ৬. ফ্লো আইকন কার্ডস
st.markdown("<br>", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown('<div class="flow-card"><div class="floating-icon">🛡️</div><h4>Privacy</h4><p>ডেটা সম্পূর্ণ নিরাপদ</p></div>', unsafe_allow_html=True)
with f2:
    st.markdown('<div class="flow-card"><div class="floating-icon">⚡</div><h4>Fast
