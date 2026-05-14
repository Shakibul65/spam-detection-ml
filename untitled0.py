import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. Page Configuration
st.set_page_config(
    page_title="Pro Spam Shield | Shakibul Hasan",
    page_icon="🛡️",
    layout="wide"
)

# 2. Custom CSS
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
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (English only)
with st.sidebar:
    st.markdown("### 👨‍💻 Developer Profile")
    st.info("**Shakibul Hasan**\n\nCSE Student & Freelancer")
    st.markdown("---")
    st.write("📍 Jamalpur, Bangladesh")
    st.write("This tool uses Machine Learning to detect spam messages.")

# 4. Header (English only)
st.markdown("""
    <div class="header-box">
        <h1 style='font-size: 35px; margin-bottom: 10px;'>🛡️ Pro Email Spam Shield</h1>
        <p style='font-size: 18px; opacity: 0.8;'>Machine Learning Powered Security | Student Project</p>
    </div>
    """, unsafe_allow_html=True)

# 5. Training Data
data = {
    'text': ['Free money now', 'Hi, how are you?', 'Claim prize', 'Meeting at 10am', 'urgent account verification'],
    'label': ['spam', 'ham', 'spam', 'ham', 'spam']
}
df = pd.DataFrame(data)

# 6. Model Training
cv = CountVectorizer()
X = cv.fit_transform(df['text'])
model = MultinomialNB()
model.fit(X, df['label'])

# 7. Analyze Message Section
st.markdown("### 🔍 Analyze Message")
user_input = st.text_area("", placeholder="Enter your message here...", height=150)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Run Security Scan"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            
            st.markdown("---")
            if prediction[0] == 'spam':
                # Results in English and Bangla (as per your image)
                st.error("🚨 RESULT: SPAM DETECTED")
                st.error("🚨 ফলাফল: এটি একটি স্প্যাম (SPAM) মেসেজ!")
                st.warning("Be careful, this message might be a security risk. সতর্ক থাকুন, এই মেসেজটি আপনার নিরাপত্তার জন্য ঝুঁকিপূর্ণ হতে পারে।")
            else:
                st.success("✅ RESULT: SAFE MESSAGE")
                st.success("✅ ফলাফল: এটি একটি নিরাপদ (SAFE) মেসেজ।")
                st.info("This message looks safe to use. এই মেসেজটি নিরাপদ মনে হচ্ছে।")
        else:
            st.warning("Please enter a message.")

# 8. Footer (English only)
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Developed by Shakibul Hasan | Machine Learning Project</p>", unsafe_allow_html=True)
