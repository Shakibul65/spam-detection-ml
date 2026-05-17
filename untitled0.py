import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
from datetime import datetime
import time

# ML Libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# =====================================================
# DATABASE
# =====================================================

def init_db():
    conn = sqlite3.connect("ai_security_suite.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scan_logs(
        message TEXT,
        prediction TEXT,
        confidence REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    return conn

conn = init_db()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Security & Real Estate Suite",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color:#f5f7fa;
}

.stButton>button {
    width:100%;
    border-radius:10px;
    height:3em;
    background:linear-gradient(90deg,#1e3c72,#2a5298);
    color:white;
    border:none;
    font-weight:bold;
}

.card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 5px 15px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SPAM AI MODEL
# =====================================================

@st.cache_resource
def load_spam_model():

    data = {
        "text":[
            "Win free money",
            "Claim your reward now",
            "Meeting at 5 pm",
            "Lunch tomorrow?",
            "Urgent verify account",
            "Project submission"
        ],

        "label":[
            "spam",
            "spam",
            "ham",
            "ham",
            "spam",
            "ham"
        ]
    }

    df = pd.DataFrame(data)

    cv = CountVectorizer()

    X = cv.fit_transform(df["text"])

    model = MultinomialNB()

    model.fit(X, df["label"])

    return cv, model

cv, spam_model = load_spam_model()

# =====================================================
# HOUSE PRICE MODEL (SVM)
# =====================================================

@st.cache_resource
def train_house_model():

    # Sample Dataset

    house_data = pd.DataFrame({

        "area":[1000,1200,1500,1800,2000,2500,3000],
        "bedrooms":[2,2,3,3,4,4,5],
        "age":[10,8,6,5,4,3,2],
        "price":[200000,250000,320000,400000,500000,650000,800000]

    })

    X = house_data[["area","bedrooms","age"]]
    y = house_data["price"]

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVR(kernel='rbf'))
    ])

    model.fit(X, y)

    return model

house_model = train_house_model()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🛡️ AI Security Suite")

    menu = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔍 Spam Detector",
            "🏡 House Price Prediction",
            "📊 Analytics",
            "🗄️ Database Logs"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

    st.title("🚀 Enterprise AI Dashboard")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total Scans","12K","+15%")
    col2.metric("Threats Blocked","2.5K","+8%")
    col3.metric("AI Accuracy","98%","+2%")
    col4.metric("System Health","99.9%","Stable")

    st.write("---")

    chart_data = pd.DataFrame(
        np.random.randint(20,100,size=(20,2)),
        columns=["Spam","Threats"]
    )

    st.line_chart(chart_data)

# =====================================================
# SPAM DETECTOR
# =====================================================

elif menu == "🔍 Spam Detector":

    st.title("🔍 AI Spam Detector")

    text = st.text_area("Enter Message")

    if st.button("Analyze Message"):

        if text:

            with st.spinner("Scanning..."):

                time.sleep(1)

                vect = cv.transform([text])

                result = spam_model.predict(vect)[0]

                prob = spam_model.predict_proba(vect)[0]

                conf = np.max(prob) * 100

                # DB Save

                c = conn.cursor()

                c.execute(
                    "INSERT INTO scan_logs VALUES (?,?,?,?)",
                    (
                        text,
                        result,
                        conf,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                )

                conn.commit()

                if result == "spam":

                    st.error(f"🚨 Spam Detected ({conf:.2f}%)")

                else:

                    st.success(f"✅ Safe Message ({conf:.2f}%)")

        else:

            st.warning("Enter a message")

# =====================================================
# HOUSE PRICE PREDICTION
# =====================================================

elif menu == "🏡 House Price Prediction":

    st.title("🏡 AI House Price Predictor (SVM)")

    st.markdown("### Enter House Information")

    area = st.slider("Area (sq ft)",1000,5000,1500)

    bedrooms = st.selectbox("Bedrooms",[1,2,3,4,5])

    age = st.slider("House Age",0,30,5)

    if st.button("Predict House Price"):

        data = pd.DataFrame({
            "area":[area],
            "bedrooms":[bedrooms],
            "age":[age]
        })

        prediction = house_model.predict(data)[0]

        st.success(f"💰 Estimated Price: ${prediction:,.0f}")

        # Visualization

        fig = px.bar(
            x=["Predicted Price"],
            y=[prediction],
            color=[prediction],
            text=[f"${prediction:,.0f}"]
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ANALYTICS
# =====================================================

elif menu == "📊 Analytics":

    st.title("📊 AI Analytics")

    fig = px.pie(
        names=["Spam","Safe","Threats"],
        values=[45,40,15],
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# DATABASE LOGS
# =====================================================

elif menu == "🗄️ Database Logs":

    st.title("🗄️ Scan History")

    df_logs = pd.read_sql_query(
        "SELECT * FROM scan_logs ORDER BY timestamp DESC",
        conn
    )

    if not df_logs.empty:

        st.dataframe(df_logs, use_container_width=True)

    else:

        st.info("No logs available")

# =====================================================
# FOOTER
# =====================================================

st.write("---")

st.caption("Developed by Shakibul Hasan | AI Security Suite 2026")
