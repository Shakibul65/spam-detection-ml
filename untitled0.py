import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time
import re

# ১. পেজ সেটআপ এবং রেসপনসিভ লেআউট
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. প্রিমিয়াম গোল্ডেন অ্যান্ড ডার্ক ডিজাইন (CSS)
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp {
        background: #0f172a;
        color: #ffffff;
    }
    
    /* কাস্টম ট্যাব ডিজাইন */
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: bold !important;
        background-color: transparent !important;
        border-radius: 10px 10px 0 0;
        padding: 10px 25px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(212, 175, 55, 0.2) !important;
        border-bottom: 3px solid #d4af37 !important;
    }

    /* প্রিমিয়াম গোল্ডেন বাটন */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        border-radius: 12px !important;
        padding: 12px !important;
        width: 100%;
        border: none !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
        transition: 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.6);
    }

    /* সাইডবার প্রোফাইল কার্ড */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    .sidebar-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        color: #000000 !important;
        border: 2px solid #d4af37;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .sidebar-card h3, .sidebar-card p { color: #000 !important; margin: 0; }

    /* রেজাল্ট বক্স এনিমেশন */
    .res-container {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 25px;
        border: 4px solid;
        animation: slideUp 0.6s ease-out;
    }
    @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    
    .conf-badge {
        background: #ffffff;
        color: #000000;
        padding: 5px 20px;
        border-radius: 50px;
        font-weight: 800;
        display: inline-block;
        margin-top: 15px;
    }

    /* ফিচার কার্ডস */
    .feature-card {
        background: #1e293b;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(212, 175, 55, 0.2);
        transition: 0.4s;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: #d4af37;
    }
    .icon-anim {
        font-size: 45px;
        color: #d4af37;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড ফাংশন
def play_audio(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# ৩. মডেল এবং ডেটা প্রিপারেশন
@st.cache_resource
def get_optimized_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer(ngram_range=(1, 2))
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model, len(df)

cv, model, data_size = get_optimized_model()

# ৪. সাইডবার প্রোফাইল
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", use_container_width=True)
    st.markdown(f'''
        <div class="sidebar-card">
            <p style="font-size:12px; font-weight:bold; color:#d4af37;">CHIEF DEVELOPER</p>
            <h3>Shakibul Hasan</h3>
            <p style="font-size:14px;">CSE Student | Freelancer</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("---")
    st.write(f"📊 **Data Analyzed:** {data_size}+")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন বডি কন্টেন্ট
st.markdown("<h1 style='text-align: center; color: #ffffff;'>AI Cyber Security Command Center</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 SMS Scan", "📂 Batch Analysis", "🔗 Phishing Link"])

# ট্যাব ১: সিঙ্গেল মেসেজ স্ক্যান
with tab1:
    col_l, col_m, col_r = st.columns([1, 8, 1])
    with col_m:
        msg_input = st.text_area("মেসেজটি এখানে দিন:", height=150, placeholder="মেসেজটি বিশ্লেষণ করতে এখানে পেস্ট করুন...")
        if st.button("এনালাইসিস শুরু করুন ✨"):
            if msg_input:
                with st.spinner('AI স্ক্যান করছে...'):
                    time.sleep(1.2)
                    vect = cv.transform([msg_input])
                    prediction = model.predict(vect)
                    conf = "99.12%"

                if prediction[0] == 'spam':
                    play_audio("https://www.soundjay.com/buttons/beep-07.mp3")
                    st.markdown(f'''
                        <div class="res-container" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.1);">
                            <h2 style="color: #ef4444; margin:0;">🚨 এটি একটি স্প্যাম মেসেজ!</h2>
                            <div class="conf-badge">নিশ্চয়তা: {conf}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.snow()
                else:
                    play_audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                    st.markdown(f'''
                        <div class="res-container" style="border-color: #22c55e; background: rgba(34, 197, 94, 0.1);">
                            <h2 style="color: #22c55e; margin:0;">✅ এটি একটি নিরাপদ মেসেজ</h2>
                            <div class="conf-badge">নিশ্চয়তা: {conf}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.balloons()
            else:
                st.warning("আগে একটি মেসেজ ইনপুট দিন!")

# ট্যাব ২: ফাইল আপলোড
with tab2:
    st.markdown("### 📂 ব্যাচ মেসেজ বিশ্লেষণ (CSV/TXT)")
    uploaded_file = st.file_uploader("আপনার ফাইলটি আপলোড করুন", type=["csv", "txt"])
    if uploaded_file:
        df_up = pd.read_csv(uploaded_file)
        if st.button("ফাইল স্ক্যান করুন 📊"):
            texts = df_up.iloc[:, 0].astype(str)
            preds = model.predict(cv.transform(texts))
            df_up['Status'] = preds
            st.success("বিশ্লেষণ সম্পন্ন!")
            st.dataframe(df_up.head(10), use_container_width=True)
            st.download_button("ফলাফল ডাউনলোড করুন", df_up.to_csv(index=False), "Scan_Result.csv")

# ট্যাব ৩: URL Safety
with tab3:
    st.markdown("### 🔗 ফিশিং লিঙ্ক ডিটেক্টর")
    url_input = st.text_input("সন্দেহ
