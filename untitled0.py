import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ১. পেজ সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide"
)

# ২. চোখের জন্য আরামদায়ক ডার্ক থিম (Soothing Dark UI)
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড - গাঢ় নীল ও কালোর সংমিশ্রণ */
    .stApp {
        background: radial-gradient(circle at top left, #1a2a6c, #b21f1f, #fdbb2d);
        background: #0f172a; /* চোখের জন্য আরামদায়ক ডার্ক স্লেট কালার */
        color: #e2e8f0;
    }
    
    /* সাইডবার ডিজাইন */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }

    /* গ্লাস ইফেক্ট কার্ড - আরও সফট লুক */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px;
        border-radius: 24px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }

    /* বাটন ডিজাইন - সফট গ্রাডিয়েন্ট */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border: none;
        color: white;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    }

    /* ইনপুট বক্স - সফট ডার্ক লুক */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        font-size: 16px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    /* ফুটার টেক্সট */
    .footer-text {
        color: #94a3b8;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইডবার (Professional Branding)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>🛡️ SpamGuard</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Developed By:**")
    st.info("**Shakibul Hasan**\n\nCSE Graduate | Freelancer")
    st.markdown("---")
    st.write("📍 Jamalpur, Bangladesh")
    st.caption("AI Model: Multinomial Naive Bayes")

# ৪. মেইন কন্টেন্ট
st.markdown("<h1 style='text-align: center; color: #f8fafc;'>🚀 Smart AI Spam Shield</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>AI প্রযুক্তির মাধ্যমে আপনার মেসেজ যাচাই করুন নিরাপদ উপায়ে।</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.15, 0.7, 0.15])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    user_input = st.text_area("মেসেজটি এখানে লিখুন:", height=180, placeholder="Type or paste your message here...")
    
    # ডেটা এবং মডেল (ট্রেনিং)
    data = {
        'text': ['Free cash prize now', 'Hi, how are you?', 'Claim reward', 'Meeting tomorrow', 'Win money now', 'Call me later'],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])

    if st.button("এনালাইসিস করুন ✨"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            prob = model.predict_proba(vect)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if prediction[0] == 'spam':
                st.markdown(f"""
                <div style="background: rgba(239, 68, 68, 0.1); padding: 25px; border-radius: 16px; border: 1px solid #ef4444;">
                    <h3 style="color: #ef4444; margin: 0;">⚠️ এটি একটি স্প্যাম মেসেজ!</h3>
                    <p style="color: #f8fafc; margin-top: 10px;">নিশ্চয়তা: {prob[0][1]*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(34, 197, 94, 0.1); padding: 25px; border-radius: 16px; border: 1px solid #22c55e;">
                    <h3 style="color: #22c55e; margin: 0;">✅ এটি একটি নিরাপদ মেসেজ।</h3>
                    <p style="color: #f8fafc; margin-top: 10px;">নিশ্চয়তা: {prob[0][0]*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("আগে একটি মেসেজ ইনপুট দিন!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ৫. ফিচার কার্ডস (নিচের সেকশন)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3 style="color:#3b82f6">🔒 Privacy</h3><p style="color:#94a3b8">আপনার ডেটা আপনার ডিভাইসেই নিরাপদ।</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3 style="color:#3b82f6">⚡ Speed</h3><p style="color:#94a3b8">মিলি-সেকেন্ডে এনালাইসিস সম্পন্ন।</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="glass-card" style="text-align: center;"><h3 style="color:#3b82f6">🎯 Accuracy</h3><p style="color:#94a3b8">উন্নত মেশিন লার্নিং প্রযুক্তি।</p></div>', unsafe_allow_html=True)

# ফুটার
st.markdown("<br><center class='footer-text'>Developed with ❤️ by <b>Shakibul Hasan</b> | CSE Graduate | 2026</center>", unsafe_allow_html=True)
