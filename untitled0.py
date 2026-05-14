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

# ২. কাস্টম সিএসএস (আরামদায়ক ডার্ক থিম)
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    /* হেডার বক্স - মার্জিত গাঢ় রঙ */
    .header-box {
        background-color: #2c3e50; /* Slate Blue-Grey */
        color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    /* বাটন ডিজাইন */
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
        border: none;
        color: #ecf0f1;
    }
    /* ইনপুট ফিল্ড */
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #bdc3c7;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইড বার
with st.sidebar:
    st.markdown("### 👨‍💻 Developer Profile")
    st.info("**Shakibul Hasan**\n\nCSE Graduate & Freelancer")
    st.markdown("---")
    st.write("এই টুলটি মেশিন লার্নিং ব্যবহার করে টেক্সট বিশ্লেষণ করে।")

# ৪. হেডার
st.markdown("""
    <div class="header-box">
        <h1 style='font-size: 40px; margin-bottom: 10px;'>🛡️ Pro Email Spam Shield</h1>
        <p style='font-size: 18px; opacity: 0.8;'>Advanced Machine Learning Security System</p>
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

# ৭. ইউজার ইন্টারফেস
st.markdown("### 🔍 Analyze Message")
user_input = st.text_area("", placeholder="আপনার মেসেজটি এখানে পেস্ট করুন...", height=150)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Run Security Scan"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            
            st.markdown("---")
            if prediction[0] == 'spam':
                st.error("🚨 **RESULT: SPAM DETECTED**\n\nএটি একটি সম্ভাব্য ক্ষতিকারক মেসেজ।")
            else:
                st.success("✅ **RESULT: SAFE MESSAGE**\n\nএটি একটি নিরাপদ মেসেজ।")
        else:
            st.warning("অনুগ্রহ করে কিছু লিখুন।")

# ৮. ফুটার
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Developed by Shakibul Hasan | Jamalpur, Bangladesh</p>", unsafe_allow_html=True)
