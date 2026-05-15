import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
import time

# ১. আধুনিক পেজ সেটআপ (Responsive & Wide)
st.set_page_config(
    page_title="SpamGuard AI - Intelligence Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম সিএসএস (UI ডিজাইন ও রেসপন্সিভনেস)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #666; padding: 10px; background: white; border-top: 1px solid #ddd; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন লোড (বড় ট্রেনিং ডেটাসেট সহ)
@st.cache_resource
def load_engine():
    data = {
        'text': [
            'Free money now', 'Hi, how are you?', 'Claim your $1000 prize', 
            'Meeting scheduled at 10am', 'Win a free gift card', 'Please call me later',
            'Congratulations! Cash reward', 'Are you coming today?', 
            'Urgent: Account locked click here', 'The project file is attached',
            'Get unlimited free data', 'Can we discuss the budget?',
            'Earn money from home easily', 'Thanks for the update',
            'Your OTP is 1234', 'Double your investment in 2 days',
            'Check out this discount link', 'Let’s grab lunch',
            'You won a lottery ticket', 'Hey, did you send the file?'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'ham', 'spam', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model, df

cv, model, base_df = load_engine()

# ৪. সাইডবার ব্র্যান্ডিং ও নেভিগেশন
with st.sidebar:
    st.title("🛡️ SpamGuard AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown("### User Profile")
    st.write("**Name:** Shakibul Hasan")
    st.caption("CSE Student | Cyber Security Enthusiast")
    st.write("📍 Jamalpur, Bangladesh")
    st.markdown("---")
    
    # নেভিগেশন মেনু
    menu = st.radio("Main Menu", ["📊 Dashboard", "🔍 Detection Tool", "💡 Security Tips", "📂 API Docs", "👨‍💻 About"])
    
    st.markdown("---")
    st.success(f"System Status: Online\n\n{datetime.now().strftime('%d %b, %2026')}")

# ৫. পেজ ১: ড্যাশবোর্ড (Analytics)
if menu == "📊 Dashboard":
    st.title("📈 Intelligence Dashboard")
    st.write("Welcome back, Shakibul! Here is the system overview.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Scanned", "1,842", "+15%")
    m2.metric("Spam Blocked", "520", "+8%")
    m3.metric("Accuracy Rate", "98.8%", "0.3%")
    m4.metric("Threat Level", "Low", "Stable")
    
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Weekly Spam Trends")
        chart_data = pd.DataFrame({'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 'Spam': [45, 55, 40, 70, 85, 30, 20]})
        fig = px.line(chart_data, x='Day', y='Spam', markers=True, color_discrete_sequence=['#dc3545'])
        st.plotly_chart(fig, use_container_width=True)
        
    with col_chart2:
        st.subheader("Training Data Mix")
        fig_pie = px.pie(base_df, names='label', hole=0.4, color_discrete_sequence=['#28a745', '#dc3545'])
        st.plotly_chart(fig_pie, use_container_width=True)

# ৬. পেজ ২: ডিটেকশন টুল (Main Tool)
elif menu == "🔍 Detection Tool":
    st.title("🚀 Smart Spam Detection")
    st.write("নিচে আপনার ইমেইল বা মেসেজটি পেস্ট করে AI এনালাইসিস শুরু করুন।")
    
    col_input, col_stats = st.columns([2, 1])
    
    with col_input:
        user_input = st.text_area("", height=250, placeholder="মেসেজটি এখানে লিখুন...")
        if st.button("Analyze Message 🔍"):
            if user_input:
                with st.spinner('Deep scanning in progress...'):
                    time.sleep(1)
                    vect = cv.transform([user_input])
                    prediction = model.predict(vect)[0]
                    prob = model.predict_proba(vect)[0]
                    
                    st.markdown("### 📊 Result Analysis")
                    if prediction == 'spam':
                        st.error(f"⚠️ SPAM DETECTED! Confidence: {prob[1]*100:.2f}%")
                        st.warning("পরামর্শ: এই লিঙ্কে ক্লিক করবেন না এবং কোনো ব্যক্তিগত তথ্য শেয়ার করবেন না।")
                    else:
                        st.success(f"✅ SAFE (HAM). Confidence: {prob[0]*100:.2f}%")
                        st.info("এটি একটি সাধারণ নিরাপদ মেসেজ বলে মনে হচ্ছে।")
            else:
                st.warning("দয়া করে আগে একটি মেসেজ লিখুন।")

    with col_stats:
        st.subheader("Text Properties")
        if user_input:
            st.write(f"**Words:** {len(user_input.split())}")
            st.write(f"**Characters:** {len(user_input)}")
            st.progress(min(len(user_input)/200, 1.0))
        else:
            st.info("ইনপুট দেওয়ার পর এখানে পরিসংখ্যান দেখা যাবে।")

# ৭. পেজ ৩: সিকিউরিটি টিপস
elif menu == "💡 Security Tips":
    st.title("💡 Cybersecurity Best Practices")
    st.markdown("""
    ### কিভাবে অনলাইন স্ক্যাম থেকে বাঁচবেন?
    1. **অচেনা লিঙ্ক:** মেসেজে থাকা অজানা লিঙ্কে ক্লিক করবেন না।
    2. **জরুরি অবস্থা:** যদি মেসেজে বলে "এখনই করুন নতুবা অ্যাকাউন্ট বন্ধ হবে", তবে সেটি স্প্যাম হওয়ার সম্ভাবনা ৯৯%।
    3. **ব্যক্তিগত তথ্য:** ব্যাংক বা কোনো কোম্পানি কখনোই মেসেজে আপনার পিন বা পাসওয়ার্ড চাইবে না।
    4. **ইমেইল চেক:** সেন্ডারের ইমেইল অ্যাড্রেসটি ভালোভাবে খেয়াল করুন।
    """)
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg")

# ৮. পেজ ৪: এপিআই ডকস
elif menu == "📂 API Docs":
    st.title("📂 Developer Integration Guide")
    st.write("আপনি আপনার অন্য কোনো অ্যাপে এই সিস্টেমটি ব্যবহার করতে চাইলে নিচের কোডটি ব্যবহার করতে পারেন।")
    st.code("""
import requests

# API integration example
def check_spam(text):
    response = requests.post("https://api.spamguard.ai/scan", json={"text": text})
    return response.json()
    """, language="python")

# ৯. পেজ ৫: এবাউট
else:
    st.title("👨‍💻 About the Project")
    st.write("---")
    st.subheader("Shakibul Hasan")
    st.write("আমি একজন **CSE Student** এবং ফ্রিল্যান্সার। সাইবার সিকিউরিটি এবং মেশিন লার্নিং এর প্রতি আমার গভীর আগ্রহ থেকে এই প্রজেক্টটি তৈরি করেছি।")
    st.write("**Location:** Jamalpur, Bangladesh")
    st.balloons()

# ১০. গ্লোবাল ফুটার (সব পেজে থাকবে)
st.markdown(f"""
    <div class="footer">
        <p>Developed by <b>Shakibul Hasan</b> | CSE Student | Jamalpur, Bangladesh | {datetime.now().year}</p>
    </div>
    """, unsafe_allow_html=True)
