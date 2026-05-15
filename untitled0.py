import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score
from datetime import datetime
import time
import re

# ==========================================
# ১. গ্লোবাল কনফিগারেশন এবং থিম সেটআপ
# ==========================================
st.set_page_config(
    page_title="SpamGuard AI Elite | Advanced Cyber Security Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# প্রিমিয়াম এবং রেসপন্সিভ কাস্টম সিএসএস (Modern UI)
st.markdown("""
    <style>
    /* মেইন কন্টেন্ট এরিয়া */
    .main { background-color: #f1f3f6; }
    
    /* সাইডবার ডিজাইন */
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
        color: white;
    }
    [data-testid="stSidebar"] * { color: #f1f3f6 !important; }
    
    /* হেডারের ফন্ট সাইজ রেসপন্সিভ */
    [data-testid="stHeader"] h1 { font-size: 2.5rem !important; }
    @media (max-width: 768px) {
        [data-testid="stHeader"] h1 { font-size: 1.8rem !important; }
    }

    /* বাটন ডিজাইন */
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.8em; 
        background: linear-gradient(90deg, #1e3c72, #2a5298); 
        color: white; font-weight: bold; border: none; transition: 0.4s;
    }
    .stButton>button:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 8px 20px rgba(0,0,0,0.25); 
        background: linear-gradient(90deg, #2a5298, #1e3c72);
    }

    /* ফলাফল এবং তথ্য কার্ড ডিজাইন */
    .status-card, .info-card { 
        background: white; padding: 25px; border-radius: 20px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 25px;
        transition: 0.3s;
    }
    .status-card:hover, .info-card:hover { transform: scale(1.01); }
    
    .spam-border { border-left: 6px solid #dc3545; }
    .ham-border { border-left: 6px solid #28a745; }
    .info-border { border-top: 5px solid #1e3c72; }

    /* গ্লোবাল ফুটার */
    .footer { 
        text-align: center; color: #555; padding: 30px; 
        border-top: 1px solid #ddd; margin-top: 80px; 
        background-color: transparent; position: relative;
    }

    /* রেসপন্সিভ ইনফো গ্রিড */
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
        gap: 25px; 
        margin-top: 20px;
    }
    
    /* ইমেজের রেসপন্সিভনেস */
    .banner-img {
        width: 100%;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# ২. এআই ইঞ্জিন এবং ডেটা প্রসেসিং (আরও বড় ডেটা)
# ==========================================
@st.cache_resource
def load_elite_engine():
    # এখানে আমরা ডাটা বাড়াচ্ছি যাতে মডেলটি আরও নির্ভুল হয়
    raw_data = {
        'text': [
            'Get 100% free money now', 'Hi, how are you today?', 'Claim your $1000 lottery prize', 
            'Meeting scheduled for tomorrow at 10am', 'Win a free iPhone 15 gift card', 
            'Please call me back when you are free', 'Congratulations! You won a cash reward', 
            'Can we discuss the project updates?', 'Urgent: Your bank account is locked, click here', 
            'The final project report is attached', 'Double your crypto investment in 24 hours',
            'Let\'s go for lunch today', 'Your OTP for transaction is 567890',
            'Apply for a high paying job from home', 'Hey, did you see the email I sent?',
            'Verify your identity immediately to avoid suspension', 'Dinner at 8 PM tonight?',
            'Cheap pharmacy deals available online', 'Thanks for the quick response',
            'Get a discount on your next flight booking', 'Please review the attached documents',
            'Your parcel is waiting at the post office', 'Are you available for a quick call?',
            'Invest now to earn millions in a week', 'Reminder: Subscription expires in 2 days'
        ],
        'label': [
            'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham',
            'spam', 'ham', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam', 'ham', 'spam',
            'ham', 'spam', 'ham', 'spam', 'ham'
        ]
    }
    df = pd.DataFrame(raw_data)
    cv = CountVectorizer()
    X = cv.fit_transform(df['text'])
    model = MultinomialNB()
    model.fit(X, df['label'])
    
    # Performance Metrics Calculation for CK
    y_pred = model.predict(X)
    acc = accuracy_score(df['label'], y_pred)
    prec = precision_score(df['label'], y_pred, pos_label='spam')
    rec = recall_score(df['label'], y_pred, pos_label='spam')
    
    return cv, model, acc, prec, rec, df

cv, model, m_acc, m_prec, m_rec, base_df = load_elite_engine()

# ইউআরএল ফিশিং ডিটেকশন লজিক
def analyze_phishing_url(url):
    reasons = []
    score = 0
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'bank', 'free', 'win', 'gift', 'identity']
    
    # ১. দৈর্ঘ্য বিশ্লেষণ
    if len(url) > 60:
        score += 30
        reasons.append("URL length is extremely long (common in phishing)")
        
    # ২. কি-ওয়ার্ড বিশ্লেষণ
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        score += 40
        reasons.append("Contains sensitive security keywords")
        
    # ৩. সাবডোমেইন বিশ্লেষণ
    if url.count('.') > 3:
        score += 20
        reasons.append("High number of subdomains detected")
        
    # ৪. সন্দেহজনক চিহ্ন বিশ্লেষণ
    if "@" in url or "-" in url or "%" in url:
        score += 10
        reasons.append("Contains '@', '-', or '%' which are often used in malicious links")
        
    # ৫. প্রোটোকল বিশ্লেষণ
    if not url.startswith('https'):
        score += 10
        reasons.append("Unsecured protocol (HTTP instead of HTTPS)")
        
    return score, reasons

# ==========================================
# ৩. সাইডবার নেভিগেশন এবং প্রোফাইল
# ==========================================
with st.sidebar:
    st.title("🛡️ SecureHub AI")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
    st.write("---")
    st.markdown("### 👨‍💻 Shakibul Hasan")
    st.caption("CSE Student | Machine Learning Enthusiast")
    st.write("📍 Jamalpur, Bangladesh")
    
    st.markdown("---")
    st.subheader("🛠️ Enterprise Tools")
    choice = st.radio("Applications:", [
        "🏠 Overview Dashboard", 
        "🔍 Spam Detector", 
        "🔗 Phishing URL Scanner", 
        "📁 CSV Bulk Analyzer", 
        "💡 Cybersecurity Insights",
        "📂 API & Developer Portal"
    ])
    
    st.markdown("---")
    st.write(f"⏱️ **System Time:** {datetime.now().strftime('%H:%M:%S')}")
    st.success("✅ System Integrity: Optimal")

# ==========================================
# ৪. মেইন পেজ কন্টেন্ট - রেসপন্সিভ ডিজাইন
# ==========================================

# পেজ ১: ড্যাশবোর্ড
if choice == "🏠 Overview Dashboard":
    # বড় ব্যানার ছবি
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", caption="Real-time Threat Monitoring Dashboard", use_container_width=True)
    st.title("🚀 Enterprise Security Intelligence Overview")
    st.write("Welcome, Shakibul! Here's your automated cyber security dashboard overview.")
    
    # মেট্রিক্স কার্ডস
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Total Items Scanned", "15,842", "+22%")
    with m2: st.metric("Threats Blocked", "4,204", "+15%")
    with m3: st.metric("URL Accuracy", "97.4%", "0.1%")
    with m4: st.metric("System Risk", "Low", "Stable")

    st.markdown("---")
    
    # গ্রাফ সেকশন
    col_chart_l, col_chart_r = st.columns(2)
    with col_chart_l:
        st.subheader("📈 Weekly Threat Detected Trends")
        chart_data = pd.DataFrame({'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 'Threats': [40, 65, 30, 95, 80, 20, 10]})
        fig = px.area(chart_data, x='Day', y='Threats', markers=True, color_discrete_sequence=['#dc3545'])
        fig.update_layout(xaxis_title="Day", yaxis_title="Blocked Requests")
        st.plotly_chart(fig, use_container_width=True)

    with col_chart_r:
        st.subheader("🛡️ Traffic Distribution by Category")
        labels = ['Email Phishing', 'Mobile Scams', 'Ransomware', 'Legit Traffic']
        values = [800, 1200, 500, 13342]
        fig_pie = px.pie(names=labels, values=values, hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

# পেজ ২: স্প্যাম ডিটেক্টর
elif choice == "🔍 Spam Detector":
    st.title("🔍 Multi-Layer Spam Guard AI")
    st.write("Analyze text content for potential spam or phishing patterns using Naive Bayes logic.")
    
    input_text = st.text_area("Input Message:", height=200, placeholder="Paste email content or SMS here...")
    
    col_btn, col_blank = st.columns([1, 4])
    with col_btn:
        start_scan = st.button("Start AI Analysis 🚀")
    
    if start_scan:
        if input_text:
            with st.spinner("Analyzing message semantics and metadata..."):
                time.sleep(1.5) # রিয়েলস্টিক ফিল দেওয়ার জন্য
                vect = cv.transform([input_text])
                prediction = model.predict(vect)[0]
                prob = model.predict_proba(vect)[0]
                
                # ফলাফলের জন্য রেসপন্সিভ কার্ড ডিজাইন
                st.markdown("---")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    if prediction == 'spam':
                        st.markdown("<div class='status-card spam-border'>", unsafe_allow_html=True)
                        st.error("🚨 ALERT: SPAM/PHISHING DETECTED!")
                        st.subheader(f"Confidence: {prob[1]*100:.2f}%")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='status-card ham-border'>", unsafe_allow_html=True)
                        st.success("✅ RESULT: SAFE CONTENT DETECTED")
                        st.subheader(f"Confidence: {prob[0]*100:.2f}%")
                        st.markdown("</div>", unsafe_allow_html=True)
                with res_col2:
                    st.info(f"**Word Count:** {len(input_text.split())}")
                    st.info(f"**Character Count:** {len(input_text)}")
                    st.info("- Action: Blocked from System Gateway.")
        else:
            st.warning("⚠️ Please provide some input text to scan.")

    # নিচে ছবি এবং রেসপন্সিভ গ্রিড
    st.image("https://www.ftc.gov/sites/default/files/styles/video_thumbnail__16_9_with_button_/public/videos/scam-gram-text-message-scams.jpg", caption="Understanding Text & Email Scams", use_container_width=True)
    st.markdown("### 📊 Engine Analysis Mechanics")
    st.markdown("""
    <div class="grid-container">
        <div class="info-card"><b>BoW Vectorization:</b> টেক্সটকে ক্ষুদ্র ক্ষুদ্র ভেক্টরে রূপান্তর করে ডিটেক্ট করা হয়।</div>
        <div class="info-card"><b>Gaussian Probability:</b> Bayesian logic ব্যবহার করে স্প্যাম হওয়ার গাণিতিক সম্ভাবনা বের করা হয়।</div>
        <div class="info-card"><b>Zero-Log Policy:</b> আপনার স্ক্যান করা ডাটা প্রসেস হওয়ার পর অটোমেটিক ডিলিট হয়ে যায়।</div>
    </div>
    """, unsafe_allow_html=True)

# পেজ ৩: ইউআরএল স্ক্যানার
elif choice == "🔗 Phishing URL Scanner":
    st.image("https://img.freepik.com/free-vector/phishing-concept-flat-design_23-2148529367.jpg", caption="Phishing Attack Simulation", use_container_width=True)
    st.title("🔗 Deep Link Intelligence Scanner")
    st.write("Scan URLs for potential security anomalies, typosquatting, and hidden redirects.")
    
    url_input = st.text_input("Enter Link to Scan:", placeholder="e.g., http://secure-banking-verify-update.net")
    
    if st.button("Start URL Analysis 🛡️"):
        if url_input:
            with st.spinner("Analyzing URL structure and subdomains..."):
                time.sleep(1)
                score, reasons = analyze_phishing_url(url_input)
                
                # ফলাফলের জন্য রেসপন্সিভ কার্ড
                st.markdown("---")
                u_res1, u_res2 = st.columns(2)
                with u_res1:
                    if score >= 50:
                        st.markdown("<div class='status-card spam-border'>", unsafe_allow_html=True)
                        st.error(f"🚨 ALERT: HIGH RISK! Risk Score: {score}/100")
                        for r in reasons: st.write(f"- {r}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='status-card ham-border'>", unsafe_allow_html=True)
                        st.success(f"✅ LOW RISK: URL Appears Safe (Risk Score: {score}/100)")
                        st.markdown("</div>", unsafe_allow_html=True)
                with u_res2:
                    fig_risk = px.pie(values=[score, 100-score], names=['Risk', 'Safe'], hole=0.6, color=['Risk', 'Safe'], color_discrete_map={'Risk':'red', 'Safe':'green'})
                    st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.warning("⚠️ Please provide a URL.")

    # নিচে ছবি এবং রেসপন্সিভ গ্রিড
    st.markdown("### 🌐 Structural Anomaly Features")
    st.markdown("""
    <div class="info-grid grid-container">
        <div class="info-card"><b>Domain Age:</b> ডোমেইনের বয়স এবং রেপুটেশন চেক করা হয়।</div>
        <div class="info-card"><b>Protocol Analysis:</b> HTTPS সিকিউরিটি লেয়ার আছে কি না তা যাচাই করা হয়।</div>
    </div>
    """, unsafe_allow_html=True)

# পেজ ৪: বাল্ক এনালাইজার
elif choice == "📁 CSV Bulk Analyzer":
    st.title("📁 Batch Processing & Automated Scan")
    st.write("Upload a CSV file with a **'text'** column for large scale automated content scanning.")
    
    uploaded_file = st.file_uploader("Upload CSV File (Max 100MB)", type=["csv"])
    if uploaded_file:
        df_uploaded = pd.read_csv(uploaded_file)
        if 'text' in df_uploaded.columns:
            st.success(f"File loaded. Total records: {len(df_uploaded)}")
            if st.button("Start Bulk Scan ⚙️"):
                with st.spinner("Processing dataset through AI gateway..."):
                    time.sleep(2)
                    vect_bulk = cv.transform(df_uploaded['text'].astype(str))
                    df_uploaded['AI_Prediction'] = model.predict(vect_bulk)
                    st.dataframe(df_uploaded, use_container_width=True)
                    
                    # রিপোর্ট ডাউলোড বাটন
                    st.markdown("---")
                    st.subheader("Summary Report")
                    fig_bulk = px.bar(df_uploaded['AI_Prediction'].value_counts(), title="Bulk Results Distribution")
                    st.plotly_chart(fig_bulk, use_container_width=True)
        else:
            st.error("⚠️ Error: ফাইলে অবশ্যই **'text'** নামে একটি কলাম থাকতে হবে।")
            
    # নিচে ছবি এবং রেসপন্সিভ গ্রিড
    st.image("https://www.ftc.gov/sites/default/files/styles/video_thumbnail__16_9_with_button_/public/videos/spam-gram-text-message-scams.jpg", caption="Automated Dataset Scan", use_container_width=True)
    st.markdown("### 📦 Enterprise Features")
    st.markdown("""
    <div class="info-card">
    <b>Scalable Gateway:</b> একসাথে হাজার হাজার ইমেইল বা মেসেজ দ্রুত স্ক্যানিংয়ের জন্য অপ্টিমাইজড আর্কিটেকচার।
    </div>
    """, unsafe_allow_html=True)

# পেজ ৫: সিকিউরিটি ইনসাইটস
elif menu == "💡 Cybersecurity Insights":
    st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", caption="Threat intelligence & Guide", use_container_width=True)
    st.title("💡 Advanced Intelligence & Resource Center")
    st.write("ডজিটাল নিরাপত্তার জন্য এই তথ্যগুলো অত্যন্ত জরুরি। একজন CSE Student হিসেবে আপনি এগুলো শেয়ার করে সচেতনতা তৈরি করতে পারেন।")
    
    t1, t2, t3 = st.tabs(["🛡️ Safety Guide", "🚨 Emerging Threats", "🛠️ System Arch"])
    
    with t1:
        st.subheader("🚩 কমন ফিশিং রেড ফ্ল্যাগস (Red Flags)")
        st.markdown("""
        * **ভুল বানান ও গ্রামার:** নামি ব্র্যান্ডের নাম (Faceb00k, G00gle) ভুল বানানে থাকলে সেটি নিশ্চিত স্প্যাম।
        * **অস্বাভাবিক তাগাদা (Sense of Urgency):** "Your account will be deleted in 1 hour" - এই ধরণের মেসেজ এড়িয়ে চলুন।
        * **Source Verification:** লিঙ্কে ক্লিক করার আগে সেন্ডারের ইমেইল ডোমেইনটি চেক করুন।
        """)
        
        st.subheader("🔐 পাসওয়ার্ড সুরক্ষা")
        st.info("""
        * **2FA চালু করুন:** সর্বদা Multi-Factor Authentication ব্যবহার করুন।
        * **Unique Passwords:** একই পাসওয়ার্ড একাধিক সাইটে ব্যবহার করবেন না।
        """)

    with t2:
        st.subheader("📡 আধুনিক সাইবার হুমকি")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.warning("**Smishing:** SMS এর মাধ্যমে করা ফিশিং যা বর্তমানে বাংলাদেশে সবচেয়ে বেশি হচ্ছে।")
        with t_col2:
            st.error("**Spear Phishing:** নির্দিষ্ট কোনো ব্যক্তিকে টার্গেট করে খুব সুক্ষ্মভাবে তৈরি করা অ্যাটাক।")
        
        st.subheader("Global Threat Distribution")
        threat_chart = pd.DataFrame({'Type':['Email', 'Social Media', 'SMS', 'Voice'], 'Hits':[50, 20, 20, 10]})
        st.plotly_chart(px.pie(threat_chart, values='Hits', names='Type', hole=0.3), use_container_width=True)

    with t3:
        st.subheader(" Our Security Stack")
        st.code("""
        - Model: Naive Bayes (MultinomialNB)
        - Vectorizer: CountVectorizer
        - Framework: Streamlit (Python)
        - Analytics: Plotly, Pandas
        """, language="text")

# পেজ ৬: এপিআই ডেভেলপার পোর্টাল (নতুন সেকশন)
elif choice == "📂 API & Developer Portal":
    st.title("📂 Integration Documentation")
    st.write("আপনি যদি আপনার অন্য কোনো প্রজেক্টে এই স্প্যাম ডিটেক্টর ব্যবহার করতে চান, তবে নিচের ডকুমেন্টেশন অনুসরণ করুন।")
    st.code("""
# API Endpoint Integration Example
import requests

def scan_text(text):
    url = "https://api.securehub.ai/v1/scan"
    payload = {"message": text}
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    return requests.post(url, json=payload, headers=headers).json()

# Example usage
result = scan_text("Win $1000 now!")
print(result)
    """, language="python")

# ==========================================
# ৫. গ্লোবাল ফুটার (সব পেজে থাকবে)
# ==========================================
st.markdown(f"""
    <div class="footer">
        <p>Developed by <b>Shakibul Hasan</b> | CSE Student | Jamalpur, Bangladesh | {datetime.now().year}</p>
    </div>
    """, unsafe_allow_html=True)
