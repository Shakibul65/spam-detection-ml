import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression  # নতুন যুক্ত করা হয়েছে
from sklearn.svm import SVC                          # নতুন যুক্ত করা হয়েছে
import sqlite3
from datetime import datetime
import time

# ==========================================
# 1. Database Implementation (Fixed Connection & Threading)
# ==========================================
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect('spam_guard_pro.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scan_logs 
                 (message TEXT, prediction TEXT, confidence REAL, timestamp TEXT)''')
    conn.commit()
    return conn

conn = get_db_connection()

# ==========================================
# 2. Page Configuration & UI Styling
# ==========================================
st.set_page_config(page_title="SpamGuard Pro | Security Suite", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background: linear-gradient(90deg, #1e3c72, #2a5298); 
        color: white; font-weight: bold; border: none;
    }
    .status-card { 
        background: white; padding: 25px; border-radius: 15px; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-left: 5px solid #1e3c72;
        color: black;
    }
    .footer { text-align: center; color: #777; padding: 40px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. AI Model Training (MultinomialNB, Logistic Regression, SVM)
# ==========================================
@st.cache_resource
def load_ai_models():
    # ডামি ডেটাসেট (ভলিউম বাড়ানোর জন্য আরও কিছু স্যাম্পল যুক্ত করা হলো)
    data = {
        'text': ['Win free cash prize', 'Hi, how are you?', 'Claim your reward', 'Meeting at 5', 
                 'Double your money', 'Project report', 'Urgent verify account', 'Lunch tomorrow',
                 'Get free iPhone now', 'Can we talk later?', 'Congratulations you won', 'Please review the document'],
        'label': ['spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham']
    }
    df = pd.DataFrame(data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    y = df['label']
    
    # ১. Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X, y)
    
    # ২. Logistic Regression
    lr_model = LogisticRegression()
    lr_model.fit(X, y)
    
    # ৩. SVM (Probability=True দেওয়া হয়েছে যাতে confidence score/proba বের করা যায়)
    svm_model = SVC(probability=True, kernel='linear')
    svm_model.fit(X, y)
    
    return cv, {"Naive Bayes": nb_model, "Logistic Regression": lr_model, "SVM": svm_model}

cv, models_dict = load_ai_models()

# ==========================================
# 4. Sidebar Navigation
# ==========================================
with st.sidebar:
    st.title("🛡️ SpamGuard Pro")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
    st.markdown("### Dev: Shakibul Hasan")
    st.caption("Computer Science & Engineering")
    st.write("---")
    
    menu = st.radio("Applications", [
        "🏠 Master Dashboard", 
        "🔍 Spam Detector AI", 
        "🔗 URL Intelligence", 
        "📁 Batch Processing",
        "🗄️ Database Logs",
        "💡 Cyber Security Insights",
        "📂 Developer API"
    ])
    st.write("---")
    st.success("System Status: Online")

# ==========================================
# 5. Main Application Logic
# ==========================================

if menu == "🏠 Master Dashboard":
    st.title("🚀 Enterprise Security Dashboard")
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Scanned", "15.2k", "+14%")
    col2.metric("Threats Blocked", "3,102", "+8%")
    col3.metric("System Health", "99.9%", "Stable")
    col4.metric("Risk Level", "Low", "Secure")
    
    st.write("---")
    st.subheader("📡 Global Attack Patterns (Live Simulation)")
    chart_data = pd.DataFrame(np.random.randint(10, 100, size=(20, 2)), columns=['Phishing', 'Malware'])
    st.line_chart(chart_data)

elif menu == "🔍 Spam Detector AI":
    st.title("🔍 Advanced Spam Analysis Engine")
    
    # অ্যালগরিদম সিলেক্ট করার অপশন যুক্ত করা হয়েছে
    selected_algo = st.selectbox("Select AI Algorithm:", ["Naive Bayes", "Logistic Regression", "SVM"])
    
    input_text = st.text_area("Enter content for analysis:", height=150, placeholder="Paste email or SMS here...")
    
    if st.button("Start AI Scan 🚀"):
        if input_text:
            with st.spinner(f'Analyzing patterns using {selected_algo}...'):
                time.sleep(1)
                
                # টেক্সট ভেক্টরাইজেশন
                vect = cv.transform([input_text])
                
                # সিলেক্টেড মডেল লোড করা
                current_model = models_dict[selected_algo]
                
                # প্রেডিকশন এবং কনফিডেন্স স্কোর হিসাব করা
                res = current_model.predict(vect)[0]
                prob = current_model.predict_proba(vect)[0]
                conf = max(prob) * 100
                
                # Database Update
                c = conn.cursor()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute('INSERT INTO scan_logs VALUES (?,?,?,?)', (input_text, res, conf, now))
                conn.commit()
                
                if res == 'spam':
                    st.error(f"🚨 ALERT: SPAM DETECTED! (Confidence: {conf:.1f}%)")
                else:
                    st.success(f"✅ CLEAN CONTENT (Confidence: {conf:.1f}%)")
                
                st.markdown(f"<div class='status-card'><b>Algorithm Used:</b> {selected_algo}<br><b>Prediction:</b> This text is flagged as <b>{res.upper()}</b> with {conf:.1f}% confidence.</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter some text first.")

elif menu == "🔗 URL Intelligence":
    st.title("🔗 Phishing Link Intelligence")
    st.image("https://img.freepik.com/free-vector/phishing-concept-flat-design_23-2148529367.jpg", width=600)
    url_input = st.text_input("Enter URL to scan:", "https://")
    
    if st.button("Scan URL Safety ⚙️"):
        risk = 85 if any(x in url_input.lower() for x in ['verify', 'login', 'win', 'prize']) else 10
        st.markdown(f"<div class='status-card'>Risk Score: {risk}/100</div>", unsafe_allow_html=True)
        if risk > 50: 
            st.error("Suspicious URL structure detected!")
        else: 
            st.success("This link matches standard safety profiles.")

elif menu == "📁 Batch Processing":
    st.title("📁 Bulk Data Processing")
    st.write("Upload a CSV file containing a 'text' column for mass analysis.")
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    if uploaded_file:
        df_batch = pd.read_csv(uploaded_file)
        st.write("Preview of data:", df_batch.head())
        if st.button("Analyze Batch"):
            st.info("Processing bulk data...")

elif menu == "🗄️ Database Logs":
    st.title("🗄️ System Scan History")
    st.write("Displaying logs directly from SQLite database.")
    
    try:
        df_logs = pd.read_sql_query("SELECT * FROM scan_logs ORDER BY timestamp DESC", conn)
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True)
            if st.button("Clear History"):
                c = conn.cursor()
                c.execute("DELETE FROM scan_logs")
                conn.commit()
                st.success("Logs cleared successfully!")
                time.sleep(0.5)
                st.rerun()
        else:
            st.info("No records found in database yet.")
    except Exception as e:
        st.error(f"Database Error: {e}")

elif menu == "💡 Cyber Security Insights":
    st.title("💡 Cybersecurity Intelligence Center")
    st.image("https://img.freepik.com/free-photo/standard-quality-control-concept-m_23-2150041848.jpg", use_container_width=True)
    
    tab1, tab2 = st.tabs(["🛡️ Safety Protocols", "📊 Attack Statistics"])
    with tab1:
        st.markdown("""
        ### Essential Safety Tips:
        * **2FA:** Enable Multi-Factor Authentication on all accounts.
        * **Link Check:** Always hover over links to see the real destination.
        * **Updates:** Keep your software and operating system updated.
        """)
    with tab2:
        fig = px.pie(names=['Phishing', 'Malware', 'Social Eng.'], values=[60, 25, 15], hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

elif menu == "📂 Developer API":
    st.title("📂 Integration & API Portal")
    st.image("https://img.freepik.com/free-vector/api-concept-illustration_114360-9397.jpg", width=500)
    st.markdown("### Python Integration Example:")
    st.code("""
import requests

def query_spamguard(text):
    api_endpoint = "https://api.spamguard.pro/v1/scan"
    payload = {"content": text}
    response = requests.post(api_endpoint, json=payload)
    return response.json()
    """, language="python")

# ==========================================
# 6. Footer
# ==========================================
st.markdown(f"<div class='footer'>Developed by **Shakibul Hasan** | CSE Student | {datetime.now().year}</div>", unsafe_allow_html=True)
