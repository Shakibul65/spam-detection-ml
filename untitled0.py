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

# ২. ডার্ক অ্যান্ড গোল্ডেন প্রো থিম (CSS)
st.markdown("""
    <style>
    .stApp {
        background: #0f172a; 
        color: #e2e8f0;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px;
        border-radius: 24px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        border: none;
        color: white;
        padding: 12px 30px;
        border-radius: 12px;
        font-weight: 600;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
    }
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-radius: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড ইফেক্ট ফাংশন
def play_sound(url):
    st.components.v1.html(f"""
        <audio autoplay>
            <source src="{url}" type="audio/mp3">
        </audio>
    """, height=0)

# ৩. ডেটা ও মডেল লোড (৫০০০+ মেসেজ অনলাইন থেকে)
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

# ৪. সাইডবার (আগের সব অপশনসহ)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #6366f1;'>🛡️ SpamGuard AI</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.write("**Developer Profile**")
    st.info("**Shakibul Hasan**\n\nCSE Student | Freelancer")
    
    st.write("**Location**")
    st.write("📍 Jamalpur, Bangladesh")
    
    st.markdown("---")
    st.write("### Project Analysis")
    st.write(f"📊 **Dataset Size:** {data_size} Messages")
    st.caption("Algorithm: SVM (Linear)")
    st.caption("UI Features: Sound & Animation")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>🚀 Smart AI Spam Shield</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("বিশ্লেষণের জন্য মেসেজটি এখানে লিখুন:", height=180, placeholder="Paste your message here...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            # প্রসেসিং এনিমেশন
            with st.spinner('AI মডেল গভীর বিশ্লেষণ করছে...'):
                time.sleep(1.5) # প্রফেশনাল ফিল দেওয়ার জন্য ছোট ডিলে
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                confidence = max(prob[0]) * 100

            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                play_sound("https://www.soundjay.com/buttons/beep-07.mp3") # এরর সাউন্ড
                st.error(f"🚨 এটি একটি স্প্যাম মেসেজ! (নিশ্চয়তা: {confidence:.2f}%)")
                st.snow() # স্প্যাম হলে বরফ পড়বে
            else:
                play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3") # সাকসেস সাউন্ড
                st.success(f"✅ এটি একটি নিরাপদ মেসেজ। (নিশ্চয়তা: {confidence:.2f}%)")
                st.balloons() # নিরাপদ হলে বেলুন উড়বে
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    st.markdown('</div>', unsafe_allow_html=True)

# ৬. স্ট্যাটাস কার্ডস
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>🔒 Privacy</h3><p>আপনার ডেটা নিরাপদ।</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>⚡ Speed</h3><p>দ্রুত ফলাফল।</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>🎯 Accuracy</h3><p>SVM ও ৫০০০+ ডেটা।</p></div>', unsafe_allow_html=True)

# ফুটার
st.markdown("<br><center style='color:#94a3b8;'>Developed with ❤️ by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
