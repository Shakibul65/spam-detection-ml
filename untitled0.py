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

# ৩. সাইড বার
with st.sidebar:
    st.markdown("### 👨‍💻 Developer Profile")
    st.info("**Shakibul Hasan**\n\nCSE Student & Freelancer")
    st.markdown("---")
    st.write("Jamalpur, Bangladesh")
    st.write("এই টুলটি মেশিন লার্নিং (Naive Bayes) অ্যালগরিদম ব্যবহার করে।")

# ৪. হেডার (এখানে আপনার রিকোয়েস্ট অনুযায়ী পরিবর্তন করা হয়েছে)
st.markdown("""
    <div class="header-box">
        <h1 style='font-size: 40px; margin-bottom: 10px;'>🛡️ Pro Email Spam Shield</h1>
        <p style='font-size: 18px; opacity: 0.8;'>Machine Learning Powered Security | Student Project</p>
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

# ৭. ইউজার ইনপুট
st.markdown("### 🔍 Analyze Message")
user_input = st.text_area("", placeholder="আপনার মেসেজটি এখানে লিখুন...", height=150)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Run Security Scan"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            
            st.markdown("---")
            if prediction[0] == 'spam':
                st.error("🚨 **RESULT: SPAM DETECTED**")
            else:
                st.success("✅ **RESULT: SAFE MESSAGE**")
        else:
            st.warning("অনুগ্রহ করে কিছু লিখুন।")

# ৮. ফুটার
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Developed by Shakibul Hasan | Machine Learning Project</p>", unsafe_allow_html=True)
