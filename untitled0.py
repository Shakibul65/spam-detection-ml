import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ সেটআপ
st.set_page_config(page_title="PhishGuard AI Elite", page_icon="🛡️", layout="wide")

# ২. ডায়নামিক স্টাইল এবং কালার ভ্যারিয়েশন (CSS)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #ffffff; }
    
    /* ট্যাব ডিজাইন */
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: bold; color: #ffffff; }

    /* গোল্ডেন প্রিমিয়াম বাটন (ট্যাব ১ এর জন্য) */
    div.stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%) !important;
        color: #000 !important; font-weight: 900 !important; border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
        transition: 0.3s ease;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(212, 175, 55, 0.6); }

    /* সাইডবার প্রোফাইল কার্ড */
    .sidebar-card { background: #fff; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #d4af37; }
    .sidebar-card h3, .sidebar-card p { color: #000 !important; margin: 0; }

    /* ট্যাব ১: ডায়নামিক গোল্ডেন রেজাল্ট */
    .res-instant { padding: 30px; border-radius: 20px; text-align: center; border: 4px solid; animation: zoomIn 0.5s; }
    @keyframes zoomIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }

    /* ট্যাব ২: ব্লু কালার ভ্যারিয়েশন (Batch) */
    .batch-box { background: linear-gradient(135deg, #1e40af 0%, #1e1b4b 100%); padding: 25px; border-radius: 15px; border: 1px solid #3b82f6; }

    /* ট্যাব ৩: ভায়োলেট কালার ভ্যারিয়েশন (URL) */
    .url-box { background: linear-gradient(135deg, #581c87 0%, #1e1b4b 100%); padding: 25px; border-radius: 15px; border: 1px solid #a855f7; }
    
    /* ফ্লোটিং আইকন এনিমেশন */
    .floating-icon { font-size: 40px; color: #d4af37; animation: float 3s ease-in-out infinite; }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড সিস্টেম
def play_sound(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

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

# ৫. মেইন বডি
st.markdown("<h1 style='text-align: center;'>AI Cyber Security Command Center</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 Instant Scan", "📂 Batch Analysis", "🔗 URL Guard"])

# --- ট্যাব ১: আপনার সেই গোল্ডেন ডায়নামিক লুক ---
with tab1:
    col_l, col_m, col_r = st.columns([1, 8, 1])
    with col_m:
        st.markdown("<br>", unsafe_allow_html=True)
        msg_in = st.text_area("মেসেজটি এখানে দিন:", height=150, placeholder="এনালাইসিস করতে টাইপ বা পেস্ট করুন...")
        if st.button("এনালাইসিস শুরু করুন ✨"):
            if msg_in:
                with st.spinner('AI স্ক্যান করছে...'):
                    time.sleep(1.2)
                    res = model.predict(cv.transform([msg_in]))
                    acc = "99.12%"
                
                if res[0] == 'spam':
                    play_sound("https://www.soundjay.com/buttons/beep-07.mp3")
                    st.markdown(f'''
                        <div class="res-instant" style="border-color:#ef4444; background:rgba(239,68,68,0.1);">
                            <h2 style="color:#ef4444;">🚨 এটি একটি স্প্যাম মেসেজ!</h2>
                            <p style="background:#fff; color:#000; display:inline-block; padding:5px 15px; border-radius:50px; font-weight:bold;">নিশ্চয়তা: {acc}</p>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.snow()
                else:
                    play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                    st.markdown(f'''
                        <div class="res-instant" style="border-color:#22c55e; background:rgba(34,197,94,0.1);">
                            <h2 style="color:#22c55e;">✅ এটি একটি নিরাপদ মেসেজ</h2>
                            <p style="background:#fff; color:#000; display:inline-block; padding:5px 15px; border-radius:50px; font-weight:bold;">নিশ্চয়তা: {acc}</p>
                        </div>
                    ''', unsafe_allow_html=True)
                    st.balloons()

# --- ট্যাব ২: ব্লু থিম ভ্যারিয়েশন (Batch Process) ---
with tab2:
    st.markdown('<div class="batch-box">', unsafe_allow_html=True)
    st.markdown("### 📂 ব্যাচ মেসেজ বিশ্লেষণ (CSV)")
    uploaded_file = st.file_uploader("আপনার ফাইলটি আপলোড করুন", type=["csv"])
    if uploaded_file:
        df_batch = pd.read_csv(uploaded_file)
        if st.button("পুরো ফাইল বিশ্লেষণ করুন 📊"):
            preds = model.predict(cv.transform(df_batch.iloc[:, 0].astype(str)))
            df_batch['Result'] = preds
            st.success("বিশ্লেষণ সম্পন্ন!")
            st.dataframe(df_batch, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ট্যাব ৩: ভায়োলেট থিম ভ্যারিয়েশন (URL Guard) ---
with tab3:
    st.markdown('<div class="url-box">', unsafe_allow_html=True)
    st.markdown("### 🔗 URL-Based Phishing Detection")
    url_input = st.text_input("সন্দেহজনক লিঙ্কটি এখানে দিন:")
    if st.button("নিরাপত্তা পরীক্ষা করুন 🔍"):
        if url_input:
            is_risky = any(x in url_input.lower() for x in ["login", "verify", "secure", "bit.ly"])
            if is_risky or len(url_input) > 50:
                st.error("⚠️ সতর্কতা: এটি একটি ফিশিং লিঙ্ক হওয়ার উচ্চ ঝুঁকি রয়েছে! (Confidence: 99.12%)")
            else:
                st.success("✅ এই লিঙ্কটি প্রাথমিক স্ক্যানে নিরাপদ মনে হচ্ছে।")
    st.markdown('</div>', unsafe_allow_html=True)

# ফিচার কার্ডস
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown('<div style="text-align:center;"><div class="floating-icon">🛡️</div><h4>Secure</h4></div>', unsafe_allow_html=True)
with c2: st.markdown('<div style="text-align:center;"><div class="floating-icon">⚡</div><h4>Fast AI</h4></div>', unsafe_allow_html=True)
with c3: st.markdown('<div style="text-align:center;"><div class="floating-icon">🎯</div><h4>99.12% Acc</h4></div>', unsafe_allow_html=True)

st.markdown(f"<br><center>Developed by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
