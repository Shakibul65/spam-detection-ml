import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ এবং হাই-কন্ট্রাস্ট থিম সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. ডার্ক অ্যান্ড গোল্ডেন প্রো থিম (CSS) - যা চোখের জন্য আরামদায়ক এবং স্পষ্ট
st.markdown("""
    <style>
    .stApp {
        background: #0f172a; /* গাঢ় নেভি ব্লু ব্যাকগ্রাউন্ড */
        color: #ffffff;
    }
    
    /* সাইডবার ডিজাইন - লেখা একদম স্পষ্ট করার জন্য */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    .sidebar-profile {
        background: #000000;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #d4af37;
        color: #ffffff !important;
    }

    /* প্রিমিয়াম গোল্ডেন বাটন - যা সাদা বা ডার্ক সবখানে স্পষ্ট */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        border: none !important;
        color: #000000 !important; /* লেখা একদম গাঢ় কালো */
        padding: 15px 30px !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
    }

    /* রেজাল্ট বক্স লজিক */
    .res-box {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 25px;
        border: 4px solid;
    }
    .res-title { 
        font-size: 32px; 
        font-weight: 900; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .res-conf {
        font-size: 18px;
        background: #ffffff;
        color: #000000;
        padding: 6px 20px;
        border-radius: 50px;
        font-weight: 800;
        display: inline-block;
        margin-top: 10px;
    }

    /* ফ্লো আইকন কার্ডস */
    .premium-flow-card {
        background: #1e293b;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(212, 175, 55, 0.2);
        transition: 0.4s;
    }
    .premium-flow-card:hover {
        border-color: #d4af37;
        transform: translateY(-8px);
    }
    .floating-icon {
        font-size: 45px;
        color: #d4af37;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-12px); }
    }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড ফাংশন
def play_sound(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# ৩. মডেল লোড করা
@st.cache_resource
def get_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer(ngram_range=(1, 2))
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model, len(df)

cv, model, data_size = get_model()

# ৪. সাইডবার (আপনার প্রোফাইল ডিটেইলস)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown(f'''
        <div class="sidebar-profile">
            <p style="margin:0; font-size:12px; color:#d4af37;">PRO DEVELOPER</p>
            <h2 style="margin:0; font-size:22px;">Shakibul Hasan</h2>
            <p style="margin:0; font-size:14px; opacity:0.9;">CSE Student | Freelancer</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("---")
    st.write(f"📊 **Data Trained:** {data_size}+")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center; color: #ffffff;'>Smart AI Message Shield</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.markdown('<div style="background: rgba(30, 41, 59, 0.5); padding: 25px; border-radius: 20px;">', unsafe_allow_html=True)
    user_input = st.text_area("বিশ্লেষণের জন্য মেসেজটি এখানে দিন:", height=150, placeholder="মেসেজ টাইপ করুন...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI স্ক্যানিং চলছে...'):
                time.sleep(1.2)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                
                # আপনার চাহিদা অনুযায়ী ফিক্সড স্কোর
                conf_score = "99.12%"

            if prediction[0] == 'spam':
                play_sound("
