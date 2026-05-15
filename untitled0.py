import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ১. আধুনিক পেজ সেটআপ (Responsive Layout)
st.set_page_config(
    page_title="SpamGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম সিএসএস (UI ডিজাইন উন্নত করার জন্য)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stTextArea>div>div>textarea {
        background-color: #ffffff;
        border-radius: 10px;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ৩. সাইডবার (Professional Branding)
with st.sidebar:
    st.title("🛡️ SpamGuard AI")
    st.markdown("---")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.subheader("Developer Details")
    st.write("**Name:** Shakibul Hasan")
    st.caption("CSE Graduate | Professional Freelancer")
    st.write("📍 Jamalpur, Bangladesh")
    st.markdown("---")
    st.info("এই AI টুলটি আপনার টেক্সট বিশ্লেষণ করে সম্ভাব্য ফিশিং বা স্প্যাম শনাক্ত করতে পারে।")

# ৪. মেইন সেকশন ডিজাইন
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🚀 Smart Spam Detection System")
    st.write("নিচে আপনার ইমেইল বা মেসেজটি পেস্ট করুন এবং দেখুন আমাদের AI মডেল এটি সম্পর্কে কী বলে।")
    
    user_input = st.text_area("", height=200, placeholder="আপনার মেসেজ এখানে লিখুন (যেমন: লটারি জেতা বা সাধারণ হাই-হ্যালো)...")
    
    # ডেটা এবং মডেল (অল্প ডেটা হলেও স্ট্রাকচার শক্তিশালী)
    data = {
        'text': [
            'Free prize money now', 'Hi, how are you?', 'Claim your $1000 prize', 
            'Meeting scheduled at 10am', 'Win a gift card', 'Please call me later',
            'Congratulations! Cash reward', 'Are you coming today?', 
            'Urgent: Account locked click here', 'The project file is attached'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])

    if st.button("Analyze Message"):
        if user_input:
            vect = cv.transform([user_input])
            prediction = model.predict(vect)
            prob = model.predict_proba(vect) # আত্মবিশ্বাস যাচাই
            
            st.markdown("### 📊 Analysis Result")
            if prediction[0] == 'spam':
                st.error(f"⚠️ SPAM DETECTED!")
                st.write(f"মডেলটি **{prob[0][1]*100:.2f}%** নিশ্চিত যে এটি একটি স্প্যাম মেসেজ।")
                st.warning("পরামর্শ: এই ধরণের মেসেজের কোনো লিঙ্কে ক্লিক করবেন না এবং ব্যক্তিগত তথ্য দেবেন না।")
            else:
                st.success(f"✅ SAFE (HAM)")
                st.write(f"মডেলটি **{prob[0][0]*100:.2f}%** নিশ্চিত যে এটি নিরাপদ।")
                st.info("এটি একটি সাধারণ যোগাযোগের মেসেজ বলে মনে হচ্ছে।")
        else:
            st.warning("দয়া করে বিশ্লেষণ করার জন্য একটি মেসেজ ইনপুট দিন।")

with col2:
    st.markdown("### 💡 কেন এটি ব্যবহার করবেন?")
    st.write("- **রিয়েল-টাইম এনালাইসিস**")
    st.write("- **গাণিতিক নির্ভুলতা**")
    st.write("- **সহজ ইউজার ইন্টারফেস**")
    
    st.markdown("---")
    st.write("### 🛠️ টেকনোলজি স্ট্যাক")
    st.code("Python\nStreamlit\nScikit-learn\nNaive Bayes", language="text")

# ৫. ফুটার
st.markdown("---")
st.markdown("<center>Developed by <b>Shakibul Hasan</b> | Powered by Machine Learning</center>", unsafe_allow_html=True)
