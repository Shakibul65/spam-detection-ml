import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ এবং থিম সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. অ্যাডভান্সড সিএসএস (ডিজাইন, এনিমেশন ও গ্লোয়িং কার্ডস)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #e2e8f0; }
    
    /* সাইডবার */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }

    /* মেইন কার্ড */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px; border-radius: 24px;
        backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); margin-bottom: 25px;
    }

    /* নিচের ৩টি প্রফেশনাল কার্ড (আকর্ষণীয় ডিজাইন) */
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        transition: all 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        background: rgba(99, 102, 241, 0.1);
        border-color: #6366f1;
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.2);
    }

    .feature-icon {
        font-size: 45px;
        margin-bottom: 15px;
        display: block;
    }

    /* বাটন */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        border: none; color: white; padding: 12px 30px;
        border-radius: 12px; font-weight: 600; width: 100%; transition: 0.3s;
    }
    
    /* রেজাল্ট কার্ডস */
    .ham-result { background: rgba(34, 197, 94, 0.1); border: 2px solid #22c55e; padding: 25px; border-radius: 20px; text-align: center; animation: pulse-green 2s infinite; }
    .spam-result { background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; padding: 25px; border-radius: 20px; text-align: center; animation: pulse-red 2s infinite; }
    
    @keyframes pulse-green { 0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(34, 197, 94, 0); } 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); } }
    @keyframes pulse-red { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
    </style>
    """, unsafe_allow_html=True)

def play_sound(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# ৩. ডেটা ও মডেল
@st.cache_resource
def get_trained_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model, len(df)

cv, model, data_size = get_trained_model()

# ৪. সাইডবার
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #6366f1;'>🛡️ SpamGuard AI</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.info("**Developer:** Shakibul Hasan\n\nCSE Student | Freelancer")
    st.markdown("---")
    st.write(f"📊 **Dataset:** {data_size} Messages")
    st.caption("Algorithm: SVM (Linear)")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>🚀 Smart AI Spam Shield</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("বিশ্লেষণের জন্য মেসেজটি এখানে লিখুন:", height=180, placeholder="Paste your message here...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI মডেল গভীর বিশ্লেষণ করছে...'):
                time.sleep(1.5)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                confidence = max(prob[0]) * 100

            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                play_sound("https://www.soundjay.com/buttons/beep-07.mp3")
                st.markdown(f'<div class="spam-result"><h2 style="color: #ef4444;">⚠️ SPAM DETECTED</h2><p>নিশ্চয়তা: {confidence:.2f}%</p></div>', unsafe_allow_html=True)
                st.snow()
            else:
                play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.markdown(f'<div class="ham-result"><h2 style="color: #22c55e;">✅ SAFE MESSAGE</h2><p>নিশ্চয়তা: {confidence:.2f}%</p></div>', unsafe_allow_html=True)
                st.balloons()
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    st.markdown('</div>', unsafe_allow_html=True)

# ৬. নিচের ৩টি আকর্ষণীয় কার্ড (Neon Icons)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔒</span>
            <h3 style="color: #6366f1;">Privacy First</h3>
            <p style="color: #94a3b8; font-size: 14px;">আপনার ডেটা লোকাল হোস্টে এনক্রিপ্টেড থাকে।</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <h3 style="color: #6366f1;">Super Fast</h3>
            <p style="color: #94a3b8; font-size: 14px;">SVM অ্যালগরিদম মিলি-সেকেন্ডে রেজাল্ট দেয়।</p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <h3 style="color: #6366f1;">AI Accuracy</h3>
            <p style="color: #94a3b8; font-size: 14px;">৫৫০০+ ট্রেইনিং ডেটা দিয়ে তৈরি হাই-প্রিসিশন মডেল।</p>
        </div>
    """, unsafe_allow_html=True)

# ফুটার
st.markdown("<br><center style='color:#94a3b8;'>Developed with ❤️ by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
