import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC # SVM অ্যালগরিদম লোড করা হয়েছে

# ১. পেজ সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. ডার্ক অ্যান্ড প্রফেশনাল থিম (CSS)
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
    }
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-radius: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইডবার
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #6366f1;'>🛡️ SpamGuard SVM</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.info("**Developer:** Shakibul Hasan\n\nCSE Student | Freelancer")
    st.markdown("---")
    st.caption("Algorithm: Support Vector Machine (SVM)")

# ৪. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>🚀 AI Spam Shield (SVM Edition)</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("আপনার মেসেজটি এখানে দিন:", height=180, placeholder="Paste email content here...")
    
    # বড় ট্রেনিং ডেটাসেট (SVM ভালো পারফর্ম করে ডেটা বাড়লে)
    data = {
        'text': [
            'Free money prize now', 'Hi, are we meeting today?', 
            'Claim your gift card reward', 'The project report is ready', 
            'Win a lottery cash prize', 'Can you call me later?',
            'Urgent account update needed', 'Let\'s have lunch tomorrow',
            'Get 100% free cash', 'Please send me the file'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    
    # SVM মডেল ইনিশিয়ালাইজ এবং ট্রেনিং
    # probability=True দেওয়া হয়েছে যাতে আমরা নিশ্চয়তার শতাংশ (percentage) দেখাতে পারি
    model = SVC(kernel='linear', probability=True) 
    model.fit(X, df['label'])

    if st.button("এনালাইসিস করুন ✨"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            prob = model.predict_proba(vect) # SVM Probability
            
            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                st.error(f"⚠️ এটি একটি স্প্যাম মেসেজ! (নিশ্চয়তা: {prob[0][1]*100:.1f}%)")
            else:
                st.success(f"✅ এটি নিরাপদ মেসেজ। (নিশ্চয়তা: {prob[0][0]*100:.1f}%)")
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='color:#94a3b8;'>Developed by <b>Shakibul Hasan</b> | CSE Student | 2026</center>", unsafe_allow_html=True)
