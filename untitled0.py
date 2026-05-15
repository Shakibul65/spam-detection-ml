অবশ্যই! ডিজাইনটিকে আরও আকর্ষণীয় এবং আধুনিক করার জন্য আমরা এখন Glassmorphism ইফেক্ট (কাঁচের মতো স্বচ্ছ লুক), অ্যানিমেটেড ব্যাকগ্রাউন্ড এবং আরও সুন্দর বাটন ডিজাইন যোগ করব। এটি এখন দেখতে কোনো প্রিমিয়াম সফটওয়্যারের মতো লাগবে।

নিচের এই কোডটি কপি করে আপনার GitHub-এর untitled0.py ফাইলে আগের সবকিছু মুছে দিয়ে পেস্ট করুন:

Python
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ১. পেজ সেটআপ এবং রেসপনসিভ কনফিগারেশন
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. কাস্টম সিএসএস (অত্যন্ত আধুনিক ডিজাইনের জন্য)
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* সাইডবার ডিজাইন */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* গ্লাস ইফেক্ট কার্ড */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin-bottom: 20px;
    }

    /* বাটন ডিজাইন */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        border: none;
        color: white;
        padding: 15px 32px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 50px;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    /* ইনপুট বক্স */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #1e1e1e !important;
        border-radius: 15px !important;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইডবার (Branding)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("---")
    st.write("**Developed By:**")
    st.info("Shakibul Hasan\n\nCSE Graduate | Freelancer")
    st.write("📍 Jamalpur, Bangladesh")
    st.markdown("---")
    st.caption("Version 2.0 - Powered by AI")

# ৪. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center; font-size: 50px;'>🚀 Smart AI Spam Shield</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>নিচের বক্সে আপনার ইমেইল বা মেসেজটি দিন এবং আমাদের AI দিয়ে সেকেন্ডেই পরীক্ষা করুন।</p>", unsafe_allow_html=True)

# কার্ড লেআউট
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    user_input = st.text_area("", height=180, placeholder="আপনার সন্দেহজনক মেসেজটি এখানে লিখুন...")
    
    # ডেটা এবং মডেল
    data = {
        'text': ['Free cash prize now', 'Hi, how are you?', 'Claim reward', 'Meeting tomorrow', 'Win money now', 'Call me later'],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])

    if st.button("এনালাইসিস শুরু করুন ✨"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            prob = model.predict_proba(vect)
            
            st.markdown("---")
            if prediction[0] == 'spam':
                st.markdown(f"""
                <div style="background: rgba(255, 75, 75, 0.2); padding: 20px; border-radius: 15px; border-left: 10px solid #ff4b4b;">
                    <h3 style="color: #ff4b4b; margin: 0;">⚠️ এটি একটি স্প্যাম মেসেজ!</h3>
                    <p>মডেলটির নিশ্চয়তা: {prob[0][1]*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(40, 167, 69, 0.2); padding: 20px; border-radius: 15px; border-left: 10px solid #28a745;">
                    <h3 style="color: #28a745; margin: 0;">✅ এটি নিরাপদ মেসেজ।</h3>
                    <p>মডেলটির নিশ্চয়তা: {prob[0][0]*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ৫. স্ট্যাটাস কার্ডস
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>🔒 সুরক্ষিত</h3><p>আপনার ডেটা কোথাও সেভ হয় না।</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>⚡ দ্রুত</h3><p>সেকেন্ডের মধ্যেই ফলাফল।</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3>🎯 নির্ভুল</h3><p>অ্যাডভান্সড এমএল অ্যালগরিদম।</p></div>', unsafe_allow_html=True)

# ফুটার
st.markdown("<br><hr><center>Developed with ❤️ by Shakibul Hasan | CSE | 2026</center>",
