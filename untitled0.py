import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime

# ১. প্রফেশনাল পেজ কনফিগারেশন
st.set_page_config(
    page_title="SpamGuard AI - Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ২. কাস্টম ডিজাইন (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: gray; padding: 10px; background: white; }
    </style>
    """, unsafe_allow_html=True)

# ৩. এআই মডেল লোড
@st.cache_resource
def train_model():
    data = {
        'text': [
            'Free prize money now', 'Hi, how are you?', 'Claim your $1000 prize', 
            'Meeting scheduled at 10am', 'Win a gift card', 'Please call me later',
            'Congratulations! Cash reward', 'Are you coming today?', 
            'Urgent: Account locked click here', 'The project file is attached',
            'Get unlimited free data', 'Can we discuss the budget?',
            'Earn money from home easily', 'Thanks for the update',
            'Your OTP is 1234', 'Double your investment in 2 days'
        ],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'ham', 'spam']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    return cv, model

cv, model = train_model()

# ৪. সাইডবার নেভিগেশন ও প্রোফাইল (এখানে CSE Student আপডেট করা হয়েছে)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("Admin Panel")
    st.markdown(f"**User:** Shakibul Hasan")
    st.caption("CSE Student | Cyber Security Enthusiast") # আপডেট করা হয়েছে
    st.markdown("---")
    
    menu = st.radio("Navigation", ["Dashboard", "Detection Tool", "Security Tips", "API Docs"])
    
    st.markdown("---")
    st.success(f"Status: System Online\n\nDate: {datetime.now().strftime('%d %b, %2026')}")

# ৫. মেইন কন্টেন্ট - ড্যাশবোর্ড লজিক
if menu == "Dashboard":
    st.title("📊 Security Intelligence Dashboard")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Scanned", "1,240", "+12%")
    m2.metric("Spam Blocked", "450", "+5%")
    m3.metric("System Accuracy", "98.2%", "0.1%")
    m4.metric("Risk Level", "Low", "Stable")

    st.markdown("### Threat Analysis Trend")
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Spam Hits': [45, 52, 38, 65, 48, 20, 15]
    })
    fig = px.line(chart_data, x='Day', y='Spam Hits', markers=True, title="Weekly Spam Detection Trend")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Detection Tool":
    st.title("🛡️ AI Content Analyzer")
    st.write("আমাদের অ্যাডভান্সড মেশিন লার্নিং মডেল ব্যবহার করে যেকোনো টেক্সট স্ক্যান করুন।")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        message = st.text_area("মেসেজটি এখানে পেস্ট করুন:", placeholder="Enter content here...", height=250)
        if st.button("Start Deep Scan 🔍"):
            if message:
                with st.spinner('Analyzing...'):
                    vect = cv.transform([message])
                    prediction = model.predict(vect)[0]
                    prob = model.predict_proba(vect)[0]

                    st.markdown("---")
                    if prediction == 'spam':
                        st.error(f"🚨 **SPAM ALERT:** This message is suspicious!")
                        st.progress(int(prob[1]*100))
                        st.write(f"Spam Confidence: {prob[1]*100:.2f}%")
                    else:
                        st.success(f"✅ **SAFE:** This message is legitimate.")
                        st.progress(int(prob[0]*100))
                        st.write(f"Safety Confidence: {prob[0]*100:.2f}%")
            else:
                st.warning("Please enter some text.")

    with col2:
        st.subheader("Live Statistics")
        if message:
            words = len(message.split())
            st.info(f"**Word Count:** {words}")
            fig_pie = px.pie(values=prob, names=['Safe', 'Spam'], hole=0.5)
            st.plotly_chart(fig_pie, use_container_width=True)

elif menu == "Security Tips":
    st.title("💡 Safety Practices")
    st.markdown("""
    * সন্দেহজনক লিঙ্কে ক্লিক করা থেকে বিরত থাকুন।
    * অজানা ইমেইল থেকে ফাইল ডাউনলোড করবেন না।
    * আপনার ওটিপি (OTP) গোপন রাখুন।
    """)

elif menu == "API Docs":
    st.title("📂 Developer Docs")
    st.code("import requests\n# Example API call structure", language="python")

# ৬. ফুটার (এখানেও CSE Student আপডেট করা হয়েছে)
st.markdown("""
    <div class="footer">
        <p>Developed by <b>Shakibul Hasan</b> | CSE Student | Jamalpur, Bangladesh</p>
    </div>
    """, unsafe_allow_html=True)
