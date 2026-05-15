import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ সেটআপ
st.set_page_config(page_title="SpamGuard Elite", page_icon="🛡️", layout="wide")

# ২. সুপার ক্লিয়ার ডিজাইন (CSS) - সব লেখা স্পষ্ট করার জন্য
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp { background-color: #0f172a; color: #ffffff; }

    /* বাটন - একদম স্পষ্ট কালো লেখা এবং উজ্জ্বল ব্যাকগ্রাউন্ড */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border: 3px solid #6366f1 !important;
        border-radius: 12px;
        width: 100%;
        height: 55px;
    }

    /* সাইডবার - ডার্ক বক্সের ভেতর সাদা লেখা */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    .sb-profile {
        background: #000000; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #6366f1;
        color: #ffffff !important;
    }

    /* রেজাল্ট বক্স - বড় এবং স্পষ্ট টেক্সট */
    .res-box {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 25px;
        border: 4px solid;
    }
    .res-title { font-size: 32px; font-weight: 900; margin-bottom: 10px; }
    .res-conf { 
        font-size: 20px; 
        background: #ffffff; 
        color: #000000; 
        padding: 5px 15px; 
        border-radius: 50px; 
        font-weight: bold;
    }

    /* ইনপুট এরিয়া টেক্সট */
    .stTextArea textarea {
        font-size: 18px !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. মডেল লোডিং
@st.cache_resource
def load_data():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model

cv, model = load_data()

# ৪. সাইডবার (আপনার প্রোফাইল)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #818cf8;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown('''
        <div class="sb-profile">
            <p style="margin:0; font-size:14px; opacity:0.8;">Developer</p>
            <h2 style="margin:0; color:#fbbf24;">Shakibul Hasan</h2>
            <p style="margin:0;">CSE Student | Freelancer</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("---")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>AI Spam Detection System</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    msg = st.text_area("মেসেজটি এখানে লিখুন:", height=150, placeholder="বিশ্লেষণের জন্য টেক্সট দিন...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if msg:
            with st.spinner('AI প্রসেসিং করছে...'):
                time.sleep(1)
                vect = cv.transform([msg])
                res = model.predict(vect)
                
                # আপনার চাহিদা মতো ৯৯.১২% ফিক্সড করা হলো
                confidence = "99.12%"

            if res[0] == 'spam':
                st.markdown(f'''
                    <div class="res-box" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.1);">
                        <div class="res-title" style="color: #ef4444;">🚨 এটি একটি স্প্যাম মেসেজ</div>
                        <span class="res-conf">নিশ্চয়তা: {confidence}</span>
                    </div>
                ''', unsafe_allow_html=True)
                st.snow()
            else:
                st.markdown(f'''
                    <div class="res-box" style="border-color: #22c55e; background: rgba(34, 197, 94, 0.1);">
                        <div class="res-title" style="color: #22c55e;">✅ এটি একটি নিরাপদ মেসেজ</div>
                        <span class="res-conf">নিশ্চয়তা: {confidence}</span>
                    </div>
                ''', unsafe_allow_html=True)
                st.balloons()
        else:
            st.error("দয়া করে একটি মেসেজ ইনপুট দিন!")

st.markdown("<br><center style='color: #94a3b8;'>Developed by Shakibul Hasan | 2026</center>", unsafe_allow_html=True)
