import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ সেটআপ এবং রেসপনসিভ কনফিগারেশন
st.set_page_config(
    page_title="SpamGuard AI Elite v3.0",
    page_icon="🛡️",
    layout="wide"
)

# ২. অ্যাডভান্সড কাস্টম সিএসএস (ডিজাইন এবং এনিমেশন)
st.markdown("""
    <style>
    /* মেইন ডার্ক ব্যাকগ্রাউন্ড */
    .stApp {
        background: #0d1117; 
        color: #e6edf3;
    }
    
    /* সাইডবার ডিজাইন */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    /* মেইন গ্লাস ইফেক্ট কার্ড */
    .glass-card {
        background: rgba(22, 27, 34, 0.8);
        padding: 35px; border-radius: 28px;
        backdrop-filter: blur(15px); border: 1px solid rgba(48, 54, 61, 0.5);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6); margin-bottom: 30px;
    }

    /* অত্যন্ত আকর্ষণীয় ফ্লো আইকন কার্ডস (নতুন ডিজাইন) */
    .akorsoniya-flow-card {
        background: radial-gradient(circle at center, #1f2937 0%, #111827 100%);
        border: 2px solid rgba(129, 140, 248, 0.2);
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        transition: all 0.5s ease-in-out;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    /* মাউস হোভার করলে গ্লোয়িং ইফেক্ট */
    .akorsoniya-flow-card:hover {
        transform: translateY(-15px) scale(1.03);
        border-color: #818cf8;
        box-shadow: 0 15px 40px rgba(129, 140, 248, 0.4);
    }
    
    /* Neon Glow জন্য Pseudo-element */
    .akorsoniya-flow-card::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle at center, rgba(129, 140, 248, 0.1) 0%, rgba(17, 24, 39, 0) 70%);
        opacity: 0; transition: opacity 0.5s;
    }
    
    .akorsoniya-flow-card:hover::before {
        opacity: 1;
    }

    /* কাস্টম আইকন ডিজাইন */
    .flow-icon {
        font-size: 60px;
        margin-bottom: 20px;
        display: block;
        background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        transition: transform 0.3s;
    }
    
    .akorsoniya-flow-card:hover .flow-icon {
        transform: scale(1.1);
    }

    /* বাটন ডিজাইন */
    .stButton>button {
        background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 100%);
        border: none; color: #111827; padding: 15px 32px;
        border-radius: 15px; font-weight: 800; font-size: 18px; text-transform: uppercase; letter-spacing: 1px; width: 100%; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(129, 140, 248, 0.3);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 25px rgba(129, 140, 248, 0.5);
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
    # ৫৫০০+ ডেটাসেট
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
    st.markdown("<h2 style='text-align: center; color: #a5b4fc;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.info("**Developer:** Shakibul Hasan\n\nCSE Student | Freelancer")
    st.markdown("---")
    st.write(f"📊 **Dataset:** {data_size} Messages")
    st.caption("Algorithm: SVM (Linear)")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center; color: #a5b4fc; font-size: 50px; font-weight: 900;'>🚀 Smart AI Spam Shield</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("বিশ্লেষণের জন্য মেসেজটি এখানে লিখুন:", height=200, placeholder="Type or paste your message here...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI মডেল গভীর বিশ্লেষণ করছে...'):
                time.sleep(1.8)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                confidence = max(prob[0]) * 100

            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                play_sound("https://www.soundjay.com/buttons/beep-07.mp3")
                st.markdown(f'<div class="spam-result"><h2 style="color: #ef4444;">⚠️ SPAM DETECTED</h2><p style="font-size: 18px;">নিচ্ছয়তা: <b>{confidence:.2f}%</b></p></div>', unsafe_allow_html=True)
                st.snow()
            else:
                play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.markdown(f'<div class="ham-result"><h2 style="color: #22c55e;">✅ SAFE MESSAGE</h2><p style="font-size: 18px;">নিচ্ছয়তা: <b>{confidence:.2f}%</b></p></div>', unsafe_allow_html=True)
                st.balloons()
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    st.markdown('</div>', unsafe_allow_html=True)

# ৬. নিচের অত্যন্ত আকর্ষণীয় ফ্লো আইকন কার্ডস (Neon Design)
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="akorsoniya-flow-card">
            <span class="flow-icon">🛡️</span>
            <h3 style="color: #a5b4fc; font-weight: 700;">Privacy Locked</h3>
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">আপনার ডেটা আপনার ডিভাইসেই নিরাপদ থাকে। আমরা কোনো তথ্য সেভ করি না।</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="akorsoniya-flow-card">
            <span class="flow-icon">⚡</span>
            <h3 style="color: #a5b4fc; font-weight: 700;">Instant Scan</h3>
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">অত্যাধুনিক SVM অ্যালগরিদম ব্যবহার করে মিলি-সেকেন্ডে ফলাফল।</p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown('<div class="akorsoniya-flow-card">', unsafe_allow_html=True)
    st.markdown('<span class="flow-icon">🎯</span>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #a5b4fc; font-weight: 700;">AI Precision</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">৫৫০০+ আসল মেসেজ দিয়ে ট্রেইন করা হাই-এ্যাকুরিসি মডেল।</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ফুটার
st.markdown("<br><hr><center style='color:#6366f1; font-weight: 600;'>Developed with ❤️ by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
