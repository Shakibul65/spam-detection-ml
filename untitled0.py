import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ১. পেজ কনফিগারেশন (টাইটেল এবং পেশাদার আইকন)
st.set_page_config(
    page_title="Pro Spam Shield | Shakibul Hasan",
    page_icon="🛡️",
    layout="wide"
)

# ২. কাস্টম সিএসএস (CSS) দিয়ে একদম রঙিন ও আধুনিক ডিজাইন
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #1a1aff;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        transition: background-color 0.3s;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #0000e6;
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #1a1aff;
    }
    .header {
        background-color: #1a1aff;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_index=True)

# ৩. সাইড বার (Sidebar) - প্রফেশনাল তথ্যের জন্য
with st.sidebar:
    # এখানে চাইলে আপনার ছবি বা লোগো যোগ করতে পারেন:
    # st.image("https://path_to_your_image.jpg", width=150)
    st.markdown("## Developed By")
    st.markdown("---")
    st.markdown("👨‍💻 **Shakibul Hasan**")
    st.markdown("🎓 **CSE Graduate**")
    st.markdown("🛠️ **Freelancer & ML Developer**")
    st.markdown(" Jamalpur, Bangladesh")
    st.markdown("---")
    st.info("আপনার Phishing Detection থিসিসের মতোই এখানে AI ব্যবহার করে স্প্যাম শনাক্ত করা হয়েছে।")

# ৪. হেডার অংশ
st.markdown("""
    <div class="header">
        <h1>🛡️ Pro Email Spam Shield</h1>
        <p style="margin-top: -10px;">AI-Powered Security | Verify Your Messages</p>
    </div>
    """, unsafe_allow_html=True)

# ৫. সিম্পল ট্রেনিং ডেটা (আপনার থিসিসের মতো এখানেও মেশিন লার্নিং ব্যবহার করা হয়েছে)
# চাইলে ভবিষ্যতে এখানে বড় ডেটাসেট ব্যবহার করতে পারেন।
data = {
    'text': ['Free lottery', 'Hi friend, how are you?', 'Claim prize now', 'Meeting at 10am', 'urgent account verification link'],
    'label': ['spam', 'ham', 'spam', 'ham', 'spam']
}
df = pd.DataFrame(data)

# ৬. ট্রেনিং প্রসেস (AI Model Building)
cv = CountVectorizer()
X = cv.fit_transform(df['text'])
model = MultinomialNB()
model.fit(X, df['label'])

# ৭. ইউজার ইন্টারফেস (User Interface)
st.markdown("---")
st.markdown("### 🔍 আপনার ইমেইলটি নিচে লিখুন:")
# 'st.text_area' বড় ইমেইল লেখার জন্য বেশি পেশাদার
user_input = st.text_area("ইমেইল বা মেসেজের বিষয়বস্তু এখানে লিখুন...", placeholder="উদাঃ Congratulation! You won a free gift card...")

col1, col2 = st.columns([1, 4]) # Predict বাটন এবং রেজাল্টের জন্য কলাম
with col1:
    predict_btn = st.button("Analyze Security")

# ৮. প্রেডিকশন এবং পেশাদার রেজাল্ট ডিসপ্লে
if predict_btn:
    if user_input:
        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        
        with col2:
            st.markdown("### 📊 বিশ্লেষণ ফলাফল:")
            if prediction[0] == 'spam':
                st.error("⚠️ সতর্কবার্তা! এটি একটি স্প্যাম (Spam) বা ফিশিং ইমেইল হওয়ার সম্ভাবনা বেশি।")
            else:
                st.success("✅ অভিনন্দন! এটি একটি নিরাপদ (Ham) ইমেইল।")
    else:
        with col2:
            st.warning("অনুগ্রহ করে কিছু লিখুন।")

# ৯. ফুটার (Footer)
st.markdown("---")
st.caption("AI-Powered Email Security | Powered by Shakibul Hasan | All Rights Reserved © 2026")
