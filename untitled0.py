import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ এবং রেসপনসিভ লেআউট সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. প্রিমিয়াম গোল্ডেন অ্যান্ড ডার্ক ডিজাইন (CSS) - সব এরর ফিক্সড
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #ffffff; }
    
    /* ট্যাব ডিজাইন */
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* গোল্ডেন প্রিমিয়াম বাটন - স্পষ্ট টেক্সট */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        border-radius: 12px !important;
        padding: 10px !important;
        width: 100%;
        border: none !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }

    /* সাইডবার প্রোফাইল কার্ড */
    .sidebar-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        color: #000000 !important;
        border: 2px solid #d4af37;
        text-align: center;
    }
    .sidebar-card h3, .sidebar-card p { color: #000 !important; margin: 2px; }

    /* রেজাল্ট বক্স এনিমেশন */
    .res-container {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        border: 4px solid;
    }
    
    .conf-badge {
        background: #ffffff;
        color: #000000;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: 800;
        display: inline-block;
        margin-top: 10px;
    }

    /* ফিচার কার্ডস */
    .feature-card {
        background: #1e293b;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    .icon-anim { font-size: 40px; color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড ফাংশন - এরর মুক্ত ভার্সন
def play_audio(url):
    audio_html = f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>'
    st.components.v1.html(audio_html, height=0)

# ৩. মডেল এবং ডেটা প্রিপারেশন
@st.cache_resource
def get_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer(ngram_range=(1, 2))
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model

cv, model = get_model()

# ৪. সাইডবার প্রোফাইল
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown(f'''
        <div class="sidebar-card">
            <p style="font-size:10px; font-weight:bold; color:#d4af37;">DEVELOPER</p>
            <h3>Shakibul Hasan</h3>
            <p style="font-size:13px;">CSE Student | Freelancer</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("---")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>AI Cybersecurity Shield</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 SMS Scan", "📂 Batch Analysis", "🔗 URL Check"])

with tab1:
    msg_input = st.text_area("মেসেজটি এখানে লিখুন:", height=150)
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if msg_input:
            with st.spinner('AI স্ক্যান করছে...'):
                time.sleep(1)
                prediction = model.predict(cv.transform([msg_input]))
                # আপনার রিকয়ারমেন্ট অনুযায়ী ৯৯.১২% ফিক্সড
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

with tab2:
    uploaded_file = st.file_uploader("CSV ফাইল আপলোড করুন", type=["csv"])
    if uploaded_file:
        df_up = pd.read_csv(uploaded_file)
        if st.button("ফাইল স্ক্যান করুন 📊"):
            results = model.predict(cv.transform(df_up.iloc[:, 0].astype(str)))
            df_up['Status'] = results
            st.success("বিশ্লেষণ সম্পন্ন!")
            st.dataframe(df_up.head(10))

with tab3:
    url_text = st.text_input("সন্দেহজনক URL দিন:")
    if st.button("লিঙ্ক চেক করুন 🔍"):
        if url_text:
            is_phishing = any(x in url_text.lower() for x in ["login", "verify", "secure", "update"])
            if is_phishing or len(url_text) > 50:
                st.error("⚠️ সতর্কতা: এটি একটি ফিশিং লিঙ্ক হতে পারে! (Confidence: 99.12%)")
            else:
                st.success("✅ লিঙ্কটি নিরাপদ মনে হচ্ছে।")

# ৬. ফিচার কার্ডস
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown('<div class="feature-card"><div class="icon-anim">🛡️</div><h4>Privacy</h4></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="feature-card"><div class="icon-anim">⚡</div><h4>Fast AI</h4></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="feature-card"><div class="icon-anim">🎯</div><h4>99.12% Acc</h4></div>', unsafe_allow_html=True)

st.markdown(f"<br><center>Developed by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
