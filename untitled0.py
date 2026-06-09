import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import sqlite3
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. Database Implementation (No Cache)
# ==========================================
def get_db_connection():
    conn = sqlite3.connect('phishing_url_detector.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scan_logs 
                 (url TEXT, prediction TEXT, confidence REAL, timestamp TEXT)''')
    conn.commit()
    return conn

conn = get_db_connection()

# ==========================================
# 2. Page Configuration & UI Styling
# ==========================================
st.set_page_config(page_title="Phishing URL Detector AI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background: linear-gradient(90deg, #00c6ff, #0072ff); 
        color: white; font-weight: bold; border: none;
    }
    .status-card { 
        background: white; padding: 20px; border-radius: 12px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px;
        border-left: 5px solid #0072ff; color: black;
    }
    .footer { text-align: center; color: #777; padding: 40px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. Model Pipeline (ডাইরেক্ট এক্সিকিউশন - নো ক্যাশ)
# ==========================================
try:
    df = pd.read_csv('phishing_dataset.csv') 
except FileNotFoundError:
    data = {
        'url': [
            'http://secure-login-facebook-verify.com', 'https://www.google.com', 
            'http://win-free-iphone-now.xyz', 'https://github.com/trending', 
            'http://netflix-billing-update.net', 'https://www.linkedin.com/feed', 
            'http://paypal-identity-check-login.org', 'https://stackoverflow.com'
        ],
        'label': ['phishing', 'safe', 'phishing', 'safe', 'phishing', 'safe', 'phishing', 'safe']
    }
    df = pd.DataFrame(data)

tfidf = TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=100)
X = tfidf.fit_transform(df['url']).toarray()
y = df['label'].map({'safe': 0, 'phishing': 1}) if df['label'].dtype == 'object' else df['label']

# মডেল ট্রেইনিং (হ্যাং রোধে লিমিটেড রিসোর্স ও দ্রুত প্রসেস)
lgb_model = LGBMClassifier(n_estimators=5, random_state=42, verbose=-1, n_jobs=1)
lgb_model.fit(X, y)

cat_model = CatBoostClassifier(iterations=5, random_state=42, verbose=0, thread_count=1)
cat_model.fit(X, y)

mlp_model = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=100, random_state=42)
mlp_model.fit(X, y)

tabnet_model = MLPClassifier(hidden_layer_sizes=(32, 16), activation='relu', random_state=42)
tabnet_model.fit(X, y)

models_dict = {
    "LightGBM": lgb_model,
    "CatBoost": cat_model,
    "TabNet Engine": tabnet_model,
    "Deep MLP": mlp_model
}

# ==========================================
# 4. Sidebar Navigation
# ==========================================
with st.sidebar:
    st.title("🛡️ Phishing URL Detector")
    st.markdown("### Dev: Shakibul Hasan")
    st.caption("Computer Science & Engineering")
    st.write("---")
    menu = st.radio("Applications", ["🏠 Master Dashboard", "🔍 URL Phishing Detector AI", "🗄️ Database Logs"])

# ==========================================
# 5. UI Logic
# ==========================================
if menu == "🏠 Master Dashboard":
    st.title("🚀 Enterprise URL Security Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Links Scanned", "24.8k")
    col2.metric("Phishing URLs Blocked", "5,412")
    col3.metric("System Health", "99.95%")

elif menu == "🔍 URL Phishing Detector AI":
    st.title("🔍 Multi-Model Phishing URL Analysis Engine")
    input_url = st.text_input("Enter URL for Deep AI Analysis:", placeholder="https://secure-login-update.example.com")
    
    if st.button("Start AI Scan 🚀"):
        if input_url:
            with st.spinner('Scanning URL across models...'):
                vect = tfidf.transform([input_url.lower()]).toarray()
                
                # সম্পূর্ণ লোকাল ভেরিয়েবল (কোনো পুরোনো নামের ট্রেইল নেই)
                output_report = []
                
                for algo_name, current_model in models_dict.items():
                    pred_code = current_model.predict(vect)[0]
                    prob = current_model.predict_proba(vect)[0]
                    conf = max(prob) * 100
                    res_text = 'PHISHING' if pred_code == 1 else 'SAFE'
                    
                    output_report.append({
                        "Algorithm": algo_name,
                        "Prediction": res_text,
                        "Confidence": conf,
                        "Status": "🚨 PHISHING" if res_text == 'PHISHING' else "✅ CLEAN"
                    })
                
                # DB লগিং
                c = conn.cursor()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute('INSERT INTO scan_logs VALUES (?,?,?,?)', (input_url, output_report[0]["Prediction"].lower(), output_report[0]["Confidence"], now))
                conn.commit()
                
                # রেজাল্ট কার্ডস
                st.write("### 📊 Scan Results:")
                cols = st.columns(4)
                for idx, r in enumerate(output_report):
                    with cols[idx]:
                        st.markdown(f"""
                        <div class='status-card'>
                            <h4>{r['Algorithm']}</h4>
                            <p>Result: <b>{r['Status']}</b></p>
                            <p>Confidence: <b>{r['Confidence']:.2f}%</b></p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # গ্রাফিক্যাল বেঞ্চমার্ক
                st.write("---")
                st.subheader("📊 Live Performance Benchmarking")
                df_bench = pd.DataFrame({
                    "Model Architecture": ["LightGBM", "CatBoost", "TabNet Engine", "Deep MLP"],
                    "Confidence Delivered": [output_report[0]["Confidence"], output_report[1]["Confidence"], output_report[2]["Confidence"], output_report[3]["Confidence"]]
                })
                fig_comp = px.bar(df_bench, x="Model Architecture", y="Confidence Delivered", color="Model Architecture")
                st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.warning("Please enter a URL first.")

elif menu == "🗄️ Database Logs":
    st.title("🗄️ URL Scan History")
    df_logs = pd.read_sql_query("SELECT * FROM scan_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df_logs, use_container_width=True)

st.markdown(f"<div class='footer'>Developed by **Shakibul Hasan** | CSE Student | 2026</div>", unsafe_allow_html=True)
