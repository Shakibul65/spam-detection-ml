import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime
import time

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="SpamGuard AI | Advanced Hub",
    page_icon="🛡️",
    layout="wide"
)

# ২. কাস্টম ডিজাইন (CSS)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: white; border-top: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই ইঞ্জিন (ডেটা এবং মডেল)
@st.cache_resource
def load_ai_model():
    data = {
        'text': [
            'Free prize money now', 'Hi, how are you?', 'Claim your $1000 prize', 
            'Meeting scheduled at 10am', 'Win a free gift card', 'Please call me later',
            'Congratulations! Cash reward', 'Are you coming today?', 
            'Urgent: Account locked click here', 'The project file is attached',
            'Get unlimited free data', 'Can we discuss the budget?',
            'Earn money from home easily', 'Thanks for the update',
            'Your OTP is 1234', 'Double your investment in 2 days',
            'Hey, did you see the email?', 'Special discount just for you',
            'I will be there in 5 mins', 'You won a lottery tickets'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model, df

cv, model, base_df = load_ai_model()

# ৪. সাইডবার নেভিগেশন
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Admin Panel")
    st.markdown("**User:** Shakibul Hasan")
    st.caption("CSE Student | Jamalpur, BD")
    st.markdown("---")
    choice = st.radio("Navigation", ["📊 Dashboard", "🔍 Detection Tool", "💡 Security Tips", "👨‍💻 Developer"])

# ৫. ড্যাশবোর্ড পেজ
if choice == "📊 Dashboard":
    st.title("📈 Security Analytics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Scanned", "1,540", "+12%")
    col2.metric("Spam Blocked", "420", "+5%")
    col3.metric("Accuracy", "98.5%", "0.2%")
    col4.metric("Risk Level", "Low", "Stable")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Weekly Spam Activity")
        chart_data = pd.DataFrame({'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 'Hits': [30, 45, 25, 60, 55, 20, 15]})
        fig = px.bar(chart_data, x='Day', y='Hits', color='Hits')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Data Distribution")
        fig_pie = px.pie(base_df, names='label', hole=0.4, color_discrete_sequence=['#28a745', '#dc3545'])
        st.plotly_chart(fig_pie, use_container_width=True)

# ৬. ডিটেকশন টুল পেজ
elif choice == "🔍 Detection Tool":
    st.title("🔍 Smart Content Scanner")
    message = st.text_area("মেসেজটি এখানে পেস্ট করুন:", placeholder="Type here...", height=200)
    
    if st.button("Analyze Now 🚀"):
        if message:
            with st.spinner('AI is analyzing...'):
                time.sleep(1)
                vect = cv.transform([message])
                prediction = model.predict(vect)[0]
                prob = model.predict_proba(vect)[0]
                
                st.markdown("---")
                if prediction == 'spam':
                    st.error(f"🚨 SPAM DETECTED! (Confidence: {prob[1]*100:.1f}%)")
                else:
                    st.success(f"✅ SAFE MESSAGE (Confidence: {prob[0]*100:.1f}%)")
                
                st.info(f"Stats: {len(message.split())} words, {len(message)} characters.")
        else:
            st.warning("Please enter text.")

# ৭. টিপস পেজ
elif choice == "💡 Security Tips":
    st.title("💡 Cyber Security Best Practices")
    st.markdown("""
    - **Check the Sender:** অচেনা ইমেইল অ্যাড্রেস থেকে সাবধান থাকুন।
    - **Urgency:** কোনো মেসেজ যদি খুব তাড়াহুড়ো করতে বলে, তবে সেটি স্প্যাম হওয়ার সম্ভাবনা বেশি।
    - **Links:** লিঙ্কে ক্লিক করার আগে মাউস রেখে আসল ইউআরএল দেখে নিন।
    """)

# ৮. ডেভেলপার পেজ
else:
    st.title("👨‍💻 About Developer")
    st.markdown("""
    **Name:** Shakibul Hasan  
    **Role:** CSE Student & Freelancer  
    **Location:** Jamalpur, Bangladesh  
    
    This project is built using Python, Streamlit, and Scikit-learn to demonstrate Machine Learning capabilities in Cyber Security.
    """)

# ৯. ফুটার
st.markdown(f'<div class="footer">Developed by Shakibul Hasan | CSE Student | {datetime.now().year}</div>', unsafe_allow_html=True)
