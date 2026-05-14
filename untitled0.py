import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="Pro Spam Shield | Shakibul Hasan",
    page_icon="🛡️",
    layout="wide"
)

# ২. কাস্টম সিএসএস (আরামদায়ক থিম)
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .header-box {
        background-color: #2c3e50; 
        color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
        height: 3.5em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #34495e;
        color: #ecf0f1;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইড বার (English & Bangla Profile)
with st.sidebar:
    st.markdown("### 👨‍💻 Developer Profile / প্রোফাইল")
    st.info("**Shakibul Hasan**\n\nCSE Student & Freelancer\nসিএসই ছাত্র এবং ফ্রিল্যান্সার")
    st.markdown("---")
    st.write("📍 Jamalpur, Bangladesh / জামালপুর, বাংলাদেশ")
    st.write("This tool uses Machine Learning (Naive Bayes) to detect spam messages.\nএই টুলটি স্প্যাম মেসেজ শনাক্ত করতে মেশিন লার্নিং ব্যবহার করে।")

# ৪. হেডার (Dual Language Header)
st.markdown("""
    <div class="header-box">
        <h1 style='font-size: 35px; margin-bottom: 10px;'>🛡️ Pro Email Spam Shield / স্প্যাম শিল্ড</h1>
        <p style='font-size: 18px; opacity: 0.8;'>Machine Learning Powered Security | Student Project</p>
        <p style='font-size: 16px; opacity: 0.7;'>মেশিন লার্নিং চালিত নিরাপত্তা ব্যবস্থা | স্টুডেন্ট প্রজেক্ট</p>
    </div>
    """, unsafe_allow_html=True)

# ৫. ট্রেনিং ডেটা
data = {
    'text': ['Free money now', 'Hi, how are you?', 'Claim prize', 'Meeting at 10am', 'urgent account verification'],
    'label': ['spam', 'ham', 'spam', 'ham', 'spam']
}
df = pd.DataFrame(data)

# ৬. মডেল ট্রেনিং
cv = CountVectorizer()
X = cv.fit_transform(df['text'])
model = MultinomialNB()
model.fit(X, df['label'])

# ৭. ইউজার ইনপুট ইন্টারফেস
st.markdown("### 🔍 Analyze Message / মেসেজটি পরীক্ষা করুন")
user_input = st.text_area("", placeholder="Enter your message here... / আপনার মেসেজটি এখানে লিখুন...", height=150)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Run Security Scan / স্ক্যান শুরু করুন"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            
            st.markdown("---")
            if prediction[0] == 'spam':
                # ফলাফল ইংরেজি ও বাংলা দুই ভাষাতেই
                st.error("🚨 **RESULT: SPAM DETECTED**")
                st.error("🚨 **ফলাফল: এটি একটি স্প্যাম (SPAM) মেসেজ!**")
                st.warning("Be careful, this message might be a security risk.\nসতর্ক থাকুন, এই মেসেজটি আপনার নিরাপত্তার জন্য ঝুঁকিপূর্ণ হতে পারে।")
            else:
                # ফলাফল ইংরেজি ও বাংলা দুই ভাষাতেই
                st.success("✅ **RESULT: SAFE MESSAGE**")
                st.success("✅ **ফলাফল: এটি একটি নিরাপদ (SAFE) মেসেজ।**")
                st.info("This message looks safe to use.\nএই মেসেজটি নিরাপদ মনে হচ্ছে।")
        else:
            st.warning("Please enter a message / অনুগ্রহ করে কিছু লিখুন।")

# ৮. ফুটার
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Developed by Shakibul Hasan | শাকিবুল হাসান</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #95a5a6; font-size: 12px;'>Machine Learning Project | মেশিন লার্নিং প্রজেক্ট</p>", unsafe_allow_html=True)
