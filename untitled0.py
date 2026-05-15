import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ সেটআপ
st.set_page_config(page_title="SpamGuard AI Elite", page_icon="🛡️", layout="wide")

# ২. ডার্ক অ্যান্ড গোল্ডেন প্রো থিম (CSS)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #e2e8f0; }
    section[data-testid="stSidebar"] { background-color: #1e293b !important; border-right: 1px solid #334155; }
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px; border-radius: 24px;
        backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        border: none; color: white; padding: 12px 30px;
        border-radius: 12px; font-weight: 600; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড ফাংশন (অনলাইন অডিও সোর্স)
def play_sound(url):
    st.components.v1.html(f"""
        <audio autoplay>
            <source src="{url}" type="audio/mp3">
        </audio>
    """, height=0)

# ৩. ডেটা ও মডেল লোড (Cache ব্যবহার করে)
@st.cache_resource
def get_trained_model():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model

cv, model = get_trained_model()

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
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("বিশ্লেষণের জন্য মেসেজটি এখানে লিখুন:", height=150)
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            # ঘুরতে থাকা প্রসেসিং আইকন (Spinner)
            with st.spinner('AI মডেল ডেটা বিশ্লেষণ করছে... দয়া করে অপেক্ষা করুন।'):
                time.sleep(2) # প্রফেশনাল ফিল দেওয়ার জন্য ২ সেকেন্ড ডিলে
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                confidence = max(prob[0]) * 100

            st.markdown("---")
            if prediction[0] == 'spam':
                # স্প্যাম হলে বিপ সাউন্ড
                play_sound("https://www.soundjay.com/buttons/beep-07.mp3")
                st.error(f"🚨 এটি একটি স্প্যাম মেসেজ! (নিশ্চয়তা: {confidence:.2f}%)")
                st.snow() # স্প্যাম হলে স্ক্রিনে তুষারপাত হবে সতর্কবার্তা হিসেবে
            else:
                # নিরাপদ হলে সাকসেস সাউন্ড
                play_sound("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3")
                st.success(f"✅ এটি একটি নিরাপদ মেসেজ। (নিশ্চয়তা: {confidence:.2f}%)")
                st.balloons() # নিরাপদ হলে স্ক্রিনে বেলুন উড়বে
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    st.markdown('</div>', unsafe_allow_html=True)

# ফুটার
st.markdown("<center style='color:#94a3b8;'>Developed by <b>Shakibul Hasan</b> | 2026</center>", unsafe_allow_html=True)
