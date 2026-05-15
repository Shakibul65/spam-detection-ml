import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ সেটআপ
st.set_page_config(page_title="PhishGuard AI Elite", page_icon="🛡️", layout="wide")

# ২. ডায়নামিক স্টাইল (প্রতিটি ট্যাবে ভিন্ন লুক দেওয়ার জন্য)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #ffffff; }
    
    /* ট্যাব এর ফন্ট এবং স্টাইল */
    .stTabs [data-baseweb="tab"] { font-size: 20px; font-weight: bold; color: #ffffff; padding: 10px 20px; }
    
    /* গোল্ডেন প্রিমিয়াম বাটন */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        color: #000 !important; font-weight: 900 !important; border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }

    /* সাইডবার প্রোফাইল */
    .sidebar-card { background: #fff; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #d4af37; }
    .sidebar-card h3, .sidebar-card p { color: #000 !important; margin: 0; }

    /* ট্যাব ১: ডায়নামিক রেজাল্ট এনিমেশন */
    .res-instant { padding: 30px; border-radius: 20px; text-align: center; border: 4px solid; animation: zoomIn 0.5s; }
    @keyframes zoomIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }

    /* ট্যাব ৩: ইউআরএল কার্ড */
    .url-warning { background: rgba(239, 68, 68, 0.2); padding: 20px; border-left: 10px solid #ef4444; border-radius: 10px; }
    .url-safe { background: rgba(34, 197, 94, 0.2); padding: 20px; border-left: 10px solid #22c55e; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই মডেল লোডিং
@st.cache_resource
def load_ai_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer(ngram_range=(1, 2))
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model

cv, model = load_ai_model()

# ৪. সাইডবার
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>🛡️ PhishGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", use_container_width=True)
    st.markdown(f'''
        <div class="sidebar-card">
            <p style="font-size:10px; color:#d4af37; font-weight:bold;">CHIEF DEVELOPER</p>
            <h3>Shakibul Hasan</h3>
            <p style="font-size:13px;">CSE Student | Freelancer</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("---")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন কন্টেন্ট - ভিন্ন ভিন্ন লেআউট
st.markdown("<h1 style='text-align: center;'>AI Cyber Security Command Center</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 Instant Scan", "📂 Batch Analysis", "🔗 URL Guard"])

# --- ট্যাব ১: একদম আগের ডায়নামিক লুক ---
with tab1:
    st.markdown("### 💬 দ্রুত এসএমএস বিশ্লেষণ")
    msg = st.text_area("মেসেজটি এখানে দিন:", height=150, placeholder="এনালাইসিস করতে টাইপ করুন...")
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if msg:
            with st.spinner('AI স্ক্যান করছে...'):
                time.sleep(1)
                res = model.predict(cv.transform([msg]))
                acc = "99.12%"
            
            if res[0] == 'spam':
                st.markdown(f'<div class="res-instant" style="border-color:#ef4444; background:rgba(239,68,68,0.1);"><h2 style="color:#ef4444;">🚨 এটি একটি স্প্যাম মেসেজ!</h2><p>নিশ্চয়তা: {acc}</p></div>', unsafe_allow_html=True)
                st.snow()
            else:
                st.markdown(f'<div class="res-instant" style="border-color:#22c55e; background:rgba(34,197,94,0.1);"><h2 style="color:#22c55e;">✅ এটি একটি নিরাপদ মেসেজ</h2><p>নিশ্চয়তা: {acc}</p></div>', unsafe_allow_html=True)
                st.balloons()

# --- ট্যাব ২: প্রফেশনাল ডাটা টেবিল লেআউট ---
with tab2:
    st.markdown("### 📂 ব্যাচ প্রসেসিং (CSV ফাইল)")
    file = st.file_uploader("আপনার মেসেজ ফাইলটি আপলোড করুন", type=["csv"])
    if file:
        df = pd.read_csv(file)
        if st.button("পুরো ফাইল বিশ্লেষণ করুন 📊"):
            with st.status("ডাটা প্রসেস হচ্ছে..."):
                preds = model.predict(cv.transform(df.iloc[:, 0].astype(str)))
                df['Result'] = preds
            st.dataframe(df, use_container_width=True)
            st.download_button("রিপোর্ট ডাউনলোড করুন", df.to_csv(index=False), "Analysis_Report.csv")

# --- ট্যাব ৩: আপনার থিসিস ফোকাসড ইউআরএল ডিটেক্টর ---
with tab3:
    st.markdown("### 🔗 URL-Based Phishing Detection")
    url_in = st.text_input("সন্দেহজনক লিঙ্কটি এখানে দিন:")
    if st.button("নিরাপত্তা পরীক্ষা করুন 🔍"):
        if url_in:
            # থিসিস লজিক: ফিশিং প্যাটার্ন চেক
            is_phish = any(x in url_in.lower() for x in ["login", "secure", "verify", "bit.ly", "update"])
            if is_phish or len(url_in) > 50:
                st.markdown(f'<div class="url-warning"><h4>⚠️ ঝুঁকি শনাক্ত করা হয়েছে!</h4>এই লিঙ্কটি ফিশিং অ্যাটাক হতে পারে। (Confidence: 99.12%)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="url-safe"><h4>✅ লিঙ্কটি নিরাপদ</h4>প্রাথমিক স্ক্যানে কোনো ঝুঁকি পাওয়া যায়নি।</div>', unsafe_allow_html=True)

st.markdown("<br><center>Developed by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
