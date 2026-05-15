import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import urllib.request

# ১. পেজ সেটআপ
st.set_page_config(page_title="SpamGuard AI Pro", page_icon="🛡️", layout="wide")

# ২. ডিজাইন (Midnight Blue Theme)
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
        border-radius: 12px; font-weight: 600; width: 100%;
    }
    .stTextArea textarea { background-color: #1e293b !important; color: #f1f5f9 !important; border-radius: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# ৩. ডেটা লোড করার ফাংশন (Online CSV থেকে)
@st.cache_resource # এটি দিলে প্রতিবার পেজ রিফ্রেশে ডেটা লোড হবে না, অ্যাপ ফাস্ট থাকবে
def load_data():
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_table(url, header=None, names=['label', 'text'])
    return df

df = load_data()

# ৪. মডেল ট্রেনিং (SVM)
cv = CountVectorizer()
X = cv.fit_transform(df['text'])
y = df['label'] # 'spam' অথবা 'ham'

model = SVC(kernel='linear', probability=True)
model.fit(X, y)

# ৫. সাইডবার
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #6366f1;'>🛡️ SpamGuard Pro</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.info("**Developer:** Shakibul Hasan\n\nCSE Student | Freelancer")
    st.markdown("---")
    st.write(f"📊 **Dataset Size:** {len(df)} messages")
    st.caption("Algorithm: SVM")

# ৬. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center;'>🚀 Advanced AI Spam Detection</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_input = st.text_area("মেসেজটি এখানে লিখুন:", height=150, placeholder="Paste your suspicious message here...")
    
    if st.button("এনালাইসিস করুন ✨"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            prob = model.predict_proba(vect)
            
            # নিশ্চিত হওয়ার শতাংশ বের করা
            confidence = max(prob[0]) * 100
            
            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                st.error(f"🚨 এটি একটি স্প্যাম মেসেজ! (নিশ্চয়তা: {confidence:.2f}%)")
            else:
                st.success(f"✅ এটি একটি নিরাপদ মেসেজ। (নিশ্চয়তা: {confidence:.2f}%)")
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center style='color:#94a3b8;'>Developed by <b>Shakibul Hasan</b> | CSE Student | 2026</center>", unsafe_allow_html=True)
