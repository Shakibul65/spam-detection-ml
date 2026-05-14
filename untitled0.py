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

# ২. কাস্টম সিএসএস (CSS) - এখানে এররটি ছিল, আমি ঠিক করে দিয়েছি
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #1a1aff;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        width: 100%;
        height: 3em;
    }
    .header-box {
        background-color: #1a1aff;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইড বার
with st.sidebar:
    st.markdown("## Developed By")
    st.markdown("👨‍💻 **Shakibul Hasan**")
    st.markdown("🎓 **CSE Graduate**")
    st.markdown("---")
    st.info("AI ব্যবহার করে স্প্যাম শনাক্তকরণ।")

# ৪. হেডার
st.markdown("""
    <div class="header-box">
        <h1>🛡️ Pro Email Spam Shield</h1>
        <p>AI-Powered Security | Verify Your Messages</p>
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
st.markdown("---")
user_input = st.text_area("মেসেজটি এখানে লিখুন:", placeholder="উদাঃ You won a prize...")

if st.button("Analyze Security"):
    if user_input:
        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        
        if prediction[0] == 'spam':
            st.error("🚨 সতর্কবার্তা! এটি একটি স্প্যাম মেসেজ।")
        else:
            st.success("✅ এটি একটি নিরাপদ মেসেজ।")
    else:
        st.warning("অনুগ্রহ করে কিছু লিখুন।")

# ৮. ফুটার
st.markdown("---")
st.caption("Developed by Shakibul Hasan | All Rights Reserved © 2026")
