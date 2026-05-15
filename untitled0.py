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
    
    /* বাটন - লেখাটি একদম কালো (Black) করা হয়েছে যাতে সাদা ব্যাকগ্রাউন্ডেও স্পষ্ট বোঝা যায় */
    .stButton>button {
        color: #000000 !important; 
        background-color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        border: 2px solid #6366f1 !important;
        border-radius: 12px;
        padding: 10px 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* সাইডবার টেক্সট - আরও উজ্জ্বল ও বড় করা হয়েছে */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    .sidebar-box {
        background: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        color: #000000 !important;
        font-weight: bold;
    }
    .sidebar-box h3, .sidebar-box p {
        color: #000000 !important;
        margin: 0;
    }

    /* রেজাল্ট টাইটেল */
    .result-title { 
        font-size: 28px; 
        font-weight: 800; 
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    /* ইনপুট বক্সের লেবেল */
    label {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. মডেল লোড
@st.cache_resource
def get_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model

cv, model = get_model()

# ৪. সাইডবার (স্পষ্ট টেক্সট)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #818cf8;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown('''
        <div class="sidebar-box">
            <p>Developer Profile</p>
            <h3>Shakibul Hasan</h3>
            <p style="font-size: 13px;">CSE Student | Freelancer</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("---")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন বডি
st.markdown("<h1 style='text-align: center; color: #ffffff;'>Smart AI Message Shield</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    user_input = st.text_area("আপনার মেসেজটি এখানে লিখুন:", height=150)
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI চেক করছে...'):
                time.sleep(1)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                conf_score = 99.12  # আপনার রিকয়ারমেন্ট অনুযায়ী ফিক্সড

            if prediction[0] == 'spam':
                st.markdown(f'<div style="background: #ef4444; padding: 20px; border-radius: 15px; text-align: center;"><div class="result-title">🚨 এটি একটি স্প্যাম মেসেজ</div><div style
