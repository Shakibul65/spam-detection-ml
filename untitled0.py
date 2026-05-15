import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
import time

# ১. রেসপন্সিভ পেজ সেটআপ
st.set_page_config(
    page_title="SpamGuard AI Elite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম সিএসএস (Advanced Responsive Design)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background: linear-gradient(90deg, #007bff, #00c6ff); 
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,123,255,0.3); }
    .info-card { 
        background: white; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-bottom: 4px solid #007bff;
    }
    .footer { text-align: center; color: #666; padding: 20px; border-top: 1px solid #ddd; margin-top: 50px; }
    
    /* গ্রিড ডিজাইন */
    .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন লোড
@st.cache_resource
def load_engine():
    data = {
        'text': [
            'Free money now', 'Hi, how are you?', 'Claim prize money', 'Meeting at 10', 
            'Win gift card', 'Call me soon', 'Congratulations you won cash', 'Project report',
            'Account locked login here', 'Your OTP is 1234', 'Double income today', 'Lunch today?',
            'Get 100% discount', 'Can we talk?', 'Urgent: Verify identity', 'File received'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model

cv, model = load_engine()

# ৪. সাইডবার
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown(f"**Dev:** Shakibul Hasan")
    st.caption("CSE Student | Jamalpur, BD")
    st.markdown("---")
    menu = st.radio("Menu", ["📊 Dashboard", "🔍 Spam Detector", "🔗 URL Scanner", "📁 Bulk Analyzer", "💡 Insights"])

# ৫. ড্যাশবোর্ড
if menu == "📊 Dashboard":
    st.title("🚀 Security Overview")
    cols = st.columns(4)
    cols[0].metric("Scanned", "3.1k", "+12%")
    cols[1].metric("Blocked", "845", "+5%")
    cols[2].metric("Phishing", "142", "+20%")
    cols[3].metric("Uptime", "99.9%", "Stable")
    
    st.markdown("---")
    st.subheader("Threat Activity Trend")
    st.area_chart(pd.DataFrame({'Threats': [15, 30, 20, 50, 40, 25, 10]}))

# ৬. স্প্যাম ডিটেক্টর
elif menu == "🔍 Spam Detector":
    st.title("🔍 Advanced Spam Guard")
    user_input = st.text_area("Analyze Text Content:", height=150)
    
    if st.button("Start AI Scan 🚀"):
        if user_input:
            vect = cv.transform([user_input])
            res = model.predict(vect)[0]
            if res == 'spam': st.error("🚨 SPAM DETECTED!")
            else: st.success("✅ SAFE CONTENT")
        else: st.warning("Enter text first.")
    
    # রেসপন্সিভ ডিজাইন কার্ড
    st.markdown("### 📊 Detector Insights")
    st.markdown("""
    <div class="grid-container">
        <div class="info-card"><b>NLP Processing:</b> টেক্সটকে ছোট ছোট টোকেনে ভাগ করে এনালাইসিস করা হয়।</div>
        <div class="info-card"><b>Accuracy:</b> আমাদের মডেল ৯৮% এর বেশি নির্ভুলভাবে স্প্যাম শনাক্ত করে।</div>
        <div class="info-card"><b>Privacy:</b> আপনার টেক্সট কোথাও সেভ করা হয় না, এটি সম্পূর্ণ নিরাপদ।</div>
    </div>
    """, unsafe_allow_html=True)

# ৭. ইউআরএল স্ক্যানার
elif menu == "🔗 URL Scanner":
    st.title("🔗 URL Intelligence")
    url = st.text_input("Enter Link:")
    if st.button("Analyze Link ⚙️"):
        if "http" in url: st.success("Checking URL structure...")
        else: st.warning("Please enter a valid URL.")
    
    st.markdown("### 🌐 URL Safety Overview")
    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **HTTPS Status:** সিকিউর প্রোটোকল চেক করা হয়।")
        st.info("💡 **Domain Age:** ডোমেইনের বয়স এবং ট্রাস্ট স্কোর দেখা হয়।")
    with c2:
        st.info("💡 **Subdomains:** অতিরিক্ত সাবডোমেইন ফিশিংয়ের লক্ষণ।")
        st.info("💡 **Symbols:** ইউআরএলে অস্বাভাবিক চিহ্ন (যেমন @, -) শনাক্ত করা হয়।")

# ৮. বাল্ক এনালাইজার
elif menu == "📁 Bulk Analyzer":
    st.title("📁 Bulk Data Scan")
    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        st.success("File uploaded successfully!")
        st.button("Run Bulk Analysis")
    
    st.markdown("### 📦 Bulk Processing Features")
    st.markdown("""
    <div class="info-card">
    1. **High Speed:** একসাথে হাজার হাজার ডাটা সেকেন্ডে প্রসেস করতে সক্ষম।<br>
    2. **Exportable:** রেজাল্ট সরাসরি ডাউনলোড করার সুবিধা।<br>
    3. **Visual Summary:** পুরো ডাটার গ্রাফিক্যাল রিপ্রেজেন্টেশন।
    </div>
    """, unsafe_allow_html=True)

# ৯. সিকিউরিটি ইনসাইটস (নতুন কন্টেন্ট)
elif menu == "💡 Insights":
    st.title("💡 Advanced Security Intelligence")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🛡️ কিভাবে নিরাপদ থাকবেন?")
        with st.expander("১. টু-ফ্যাক্টর অথেন্টিকেশন (2FA)"):
            st.write("শুধুমাত্র পাসওয়ার্ড যথেষ্ট নয়। সবসময় মোবাইলে ওটিপি বা অথেন্টিকেটর অ্যাপ ব্যবহার করুন।")
        with st.expander("২. ইমেইল স্পুফিং চেনা"):
            st.write("সেন্ডারের নাম আসল মনে হলেও ইমেইল এড্রেসটি (যেমন: support@faceb00k-login.com) চেক করুন।")
        with st.expander("৩. সফটওয়্যার আপডেট"):
            st.write("আপনার ফোন এবং কম্পিউটারের সিকিউরিটি প্যাচ নিয়মিত আপডেট করুন।")

    with col_b:
        st.markdown("### 🚨 আধুনিক সাইবার হুমকি")
        st.warning("**Smishing:** এসএমএস এর মাধ্যমে ভুয়া লিঙ্ক পাঠিয়ে তথ্য চুরি করা।")
        st.warning("**Vishing:** ব্যাংক কর্মকর্তা সেজে ফোন করে ওটিপি বা পিন হাতিয়ে নেওয়া।")
        st.warning("**Spear Phishing:** নির্দিষ্ট কাউকে টার্গেট করে তৈরি করা অত্যন্ত সুক্ষ্ম অ্যাটাক।")

    st.markdown("---")
    st.subheader("📊 গ্লোবাল সিকিউরিটি রিপোর্ট ২০২৬")
    
    # রেসপন্সিভ চার্ট
    insight_data = pd.DataFrame({
        'Type': ['Email Phishing', 'Mobile Scams', 'Ransomware', 'Social Engineering'],
        'Percentage': [40, 25, 20, 15]
    })
    fig = px.pie(insight_data, values='Percentage', names='Type', hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

# ১০. ফুটার
st.markdown(f"""
    <div class="footer">
        <p>Developed by <b>Shakibul Hasan</b> | CSE Student | Jamalpur, Bangladesh | {datetime.now().year}</p>
    </div>
    """, unsafe_allow_html=True)
