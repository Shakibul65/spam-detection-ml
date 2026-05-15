import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from datetime import datetime
import time

# ==========================================
# ১. পেজ কনফিগারেশন ও থিম (Responsive Layout)
# ==========================================
st.set_page_config(
    page_title="SpamGuard AI | Advanced Security Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# কাস্টম সিএসএস (UI সৌন্দর্য বাড়ানোর জন্য)
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stApp { max-width: 100%; }
    .css-1d391kg { background-color: #1a1c24; }
    .stat-card {
        padding: 20px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #666;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #ddd;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# ২. ডামি লার্জ ডেটাসেট ও মডেল ট্রেনিং
# ==========================================
@st.cache_resource
def initialize_ai_engine():
    # এখানে আমরা ডাটা বাড়াচ্ছি যাতে মডেলটি আরও স্মার্ট হয়
    raw_data = {
        'text': [
            'Get 100% free money now', 'Hi, how are you today?', 'Claim your $1000 lottery prize', 
            'Meeting scheduled for tomorrow at 10am', 'Win a free iPhone 15 gift card', 
            'Please call me back when you are free', 'Congratulations! You won a cash reward', 
            'Can we discuss the project updates?', 'Urgent: Your bank account is locked, click here', 
            'The final project report is attached', 'Double your crypto investment in 24 hours',
            'Let\'s go for lunch today', 'Your OTP for transaction is 567890',
            'Apply for a high paying job from home', 'Hey, did you see the email I sent?',
            'Verify your identity immediately to avoid suspension', 'Dinner at 8 PM tonight?',
            'Cheap pharmacy deals available online', 'Thanks for the quick response',
            'Get a discount on your next flight booking', 'Please review the attached documents',
            'Your parcel is waiting at the post office', 'Are you available for a quick call?',
            'Invest now to earn millions in a week', 'Reminder: Subscription expires in 2 days'
        ],
        'label': [
            'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham',
            'spam', 'ham', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam',
            'ham', 'spam', 'ham', 'spam', 'ham'
        ]
    }
    df = pd.DataFrame(raw_data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model, df

cv, model, base_df = initialize_ai_engine()

# ==========================================
# ৩. সাইডবার নেভিগেশন (Student Profile)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
    st.title("User Profile")
    st.write("---")
    st.markdown("### 👨‍💻 Shakibul Hasan")
    st.caption("CSE Student | Machine Learning Enthusiast")
    st.info("📍 Jamalpur, Bangladesh")
    
    st.markdown("---")
    st.subheader("🛠️ Navigation")
    choice = st.selectbox("Go to:", [
        "🏠 Overview Dashboard", 
        "🔍 Spam Detection Tool", 
        "📈 Analytics & Insights", 
        "🛡️ Security Best Practices", 
        "📂 Developer API",
        "👨‍💻 About Developer"
    ])
    
    st.markdown("---")
    st.write("⏱️ **System Time:**", datetime.now().strftime("%H:%M:%S"))
    st.success("✅ System Integrity: Stable")

# ==========================================
# ৪. পেজ ১: ওভারভিউ ড্যাশবোর্ড
# ==========================================
if choice == "🏠 Overview Dashboard":
    st.title("📊 Security Intelligence Overview")
    st.write("Welcome back, Shakibul! Here's what's happening with your SpamGuard AI system.")
    
    # ইনডেক্স কার্ডস
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Scanned", "5,842", "+15%")
    with c2:
        st.metric("Spam Identified", "1,204", "+8%")
    with c3:
        st.metric("Ham (Safe)", "4,638", "-2%")
    with c4:
        st.metric("Uptime", "99.9%", "Stable")

    st.markdown("---")
    
    # ডামি গ্রাফ
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("📈 Threat Activity (Last 7 Days)")
        chart_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Spam': [120, 150, 110, 180, 200, 90, 70],
            'Ham': [400, 420, 380, 450, 480, 550, 600]
        })
        fig = px.area(chart_data, x='Day', y=['Spam', 'Ham'], color_discrete_sequence=['red', 'green'])
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🛡️ Distribution by Category")
        labels = ['Phishing', 'Promotional', 'Legit', 'Social']
        values = [450, 600, 4000, 792]
        fig_pie = px.pie(names=labels, values=values, hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# ৫. পেজ ২: স্প্যাম ডিটেকশন টুল
# ==========================================
elif choice == "🔍 Spam Detection Tool":
    st.title("🔍 Advanced AI Content Scanner")
    st.write("Paste your message below for deep analysis using our Naive Bayes AI engine.")

    input_text = st.text_area("Input Message:", height=250, placeholder="Type or paste email/SMS content here...")
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        analyze = st.button("Run Scan 🚀")
    
    if analyze:
        if input_text:
            with st.spinner("Analyzing message patterns and metadata..."):
                time.sleep(1.5) # রিয়েলস্টিক ফিল দেওয়ার জন্য
                vect = cv.transform([input_text])
                prediction = model.predict(vect)[0]
                probability = model.predict_proba(vect)[0]
                
                # ফলাফল উইজেট
                st.markdown("---")
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    if prediction == 'spam':
                        st.error("🚨 RESULT: POSITIVE SPAM")
                        st.subheader(f"Confidence: {probability[1]*100:.2f}%")
                    else:
                        st.success("✅ RESULT: NEGATIVE (SAFE)")
                        st.subheader(f"Confidence: {probability[0]*100:.2f}%")
                
                with res_col2:
                    st.write("**Analysis Details:**")
                    st.info(f"- Word Count: {len(input_text.split())}")
                    st.info(f"- Character Count: {len(input_text)}")
                    st.info("- Algorithm: Multinomial Naive Bayes")
        else:
            st.warning("⚠️ Please enter some text to scan.")

# ==========================================
# ৬. পেজ ৩: অ্যানালিটিক্স
# ==========================================
elif choice == "📈 Analytics & Insights":
    st.title("📊 Data Analytics")
    st.write("Detailed breakdown of model
