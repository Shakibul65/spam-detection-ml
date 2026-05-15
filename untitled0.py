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

# ২. অ্যাডভান্সড সিএসএস (Glowing Icons & Cards)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #e2e8f0; }
    
    /* Glowing Success Card */
    .ham-result {
        background: rgba(34, 197, 94, 0.1);
        border: 2px solid #22c55e;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
        animation: pulse-green 2s infinite;
    }
    
    /* Glowing Error Card */
    .spam-result {
        background: rgba(239, 68, 68, 0.1);
        border: 2px solid #ef4444;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
        animation: pulse-red 2s infinite;
    }

    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(34, 197, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }

    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    .icon-img {
        width: 80px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড ফাংশন
def play_sound(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# ৩. ডেটা ও মডেল লোড
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
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>🚀 AI Message Analyzer</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

with col2:
    st.markdown('<div style="background: rgba(30, 41, 59, 0.7); padding: 30px; border-radius: 24px; backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05);">', unsafe_allow_html=True)
    user_input = st.text_area("মেসেজটি এখানে লিখুন:", height=150)
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI স্ক্যান করছে...'):
                time.sleep(1.5)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                confidence = max(prob[0]) * 100

            st.markdown("<br>", unsafe_allow_html=True)
            
            if prediction[0] == 'spam':
                play_sound("https://www.soundjay.com/buttons/beep-07.mp3")
                st.markdown(f"""
                    <div class="spam-result">
                        <img src="https://cdn-icons-png.flaticon.com/512/595/595067.png" class="icon-img">
                        <h2 style="color: #ef4444; margin:0;">SPAM DETECTED!</h2>
                        <p style="font-size: 18px;">মডেলটি <b>{confidence:.2f}%</b> নিশ্চিত যে এটি ক্ষতিকর।</p>
                    </div>
                """, unsafe_allow_html=True)
                st.snow()
            else:
                play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.markdown(f"""
                    <div class="ham-result">
                        <img src="https://cdn-icons-png.flaticon.com/512/1161/1161388.png" class="icon-img">
                        <h2 style="color: #22c55e; margin:0;">SAFE MESSAGE</h2>
                        <p style="font-size: 18px;">মডেলটি <b>{confidence:.2f}%</b> নিশ্চিত যে এটি নিরাপদ।</p>
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()
        else:
            st.warning("মেসেজ বক্সটি খালি!")
    st.markdown('</div>', unsafe_allow_html=True)

# ফুটার
st.markdown("<br><center style='color:#94a3b8;'>Developed by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
