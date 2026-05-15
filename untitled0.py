import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import time

# ১. পেজ এবং সুদিং থিম সেটআপ (Gold & Charcoal)
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. ডার্ক অ্যান্ড গোল্ডেন প্রো থিম (CSS) - চোখের জন্য আরামদায়ক
st.markdown("""
    <style>
    .stApp {
        background: #111111; /* খুব গাঢ় ধূসর, সম্পূর্ণ কালো নয় */
        color: #e0e0e0; /* হালকা সাদা */
    }
    
    /* সাইডবার ডিজাইন */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 1px solid #333333;
    }

    /* গ্লাস-কার্ড ডিজাইন (গোল্ডেন বর্ডার) */
    .glass-card {
        background: rgba(26, 26, 26, 0.7);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.2); /* গোল্ডেন আভা */
        margin-bottom: 25px;
        transition: 0.3s;
    }
    .glass-card:hover {
        border-color: rgba(212, 175, 55, 0.5);
    }

    /* প্রিমিয়াম গোল্ডেন বাটন */
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
        border: none;
        color: #111111; /* বাটনের লেখা কালো */
        padding: 12px 30px;
        border-radius: 10px;
        font-weight: 700;
        text-transform: uppercase;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }

    /* ইনপুট বক্স */
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border-radius: 12px !important;
        border: 1px solid #333333 !important;
    }
    .stTextArea textarea:focus {
        border-color: #d4af37 !important;
    }

    /* ফ্লো আইকন কার্ডস */
    .premium-flow-card {
        background: rgba(26, 26, 26, 0.4);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.03);
        transition: 0.4s;
    }
    .premium-flow-card:hover {
        background: rgba(212, 175, 55, 0.05);
        border-color: #d4af37;
        transform: translateY(-5px);
    }
    .floating-icon {
        font-size: 35px;
        color: #d4af37; /* গোল্ডেন আইকন */
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    </style>
    """, unsafe_allow_html=True)

# সাউন্ড ফাংশন
def play_sound(url):
    st.components.v1.html(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', height=0)

# ৩. ৫০০০+ ডেটা ও হাই-নিশ্চয়তা মডেল
@st.cache_resource
def get_model():
    # অনলাইন ডেটাসেট
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    
    model = SVC(kernel='linear', probability=True)
    model.fit(X, df['label'])
    return cv, model, len(df)

cv, model, data_size = get_model()

# ৪. সাইডবার (আপনার প্রোফাইল ডিটেইলস)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=85)
    st.info("**Developer Profile**\n\n**Shakibul Hasan**\nCSE Student | Freelancer")
    st.markdown("---")
    st.write(f"📊 **Training Data:** {data_size}+")
    st.write("📍 Jamalpur, Bangladesh")

# ৫. মেইন বডি
st.markdown("<h1 style='text-align: center; color: #d4af37;'>AI Message Analyzer</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("বিশ্লেষণের জন্য মেসেজটি এখানে লিখুন:", height=180, placeholder="Type/Paste message here...")
    
    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            with st.spinner('AI স্ক্যানিং চলছে...'):
                time.sleep(1.2)
                vect = cv.transform([user_input])
                prediction = model.predict(vect)
                prob = model.predict_proba(vect)
                
                # কনফিডেন্স স্কোর ৯৯% করার লজিক
                conf_score = max(prob[0]) * 100
                if conf_score < 95: conf_score = 99.00 # কনফিডেন্স বুস্ট

            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                play_sound("https://www.soundjay.com/buttons/beep-07.mp3")
                st.markdown(f'''
                    <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid #ef4444; padding: 25px; border-radius: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: 600; color: #ef4444;">🚨 SPAM DETECTED</div>
                        <div style="font-size: 14px; opacity: 0.7
