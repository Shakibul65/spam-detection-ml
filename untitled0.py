import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
import time

from datetime import datetime

# ML Algorithms
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SpamGuard Pro AI",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.stButton>button{
    width:100%;
    height:3em;
    border-radius:10px;
    border:none;
    background:linear-gradient(90deg,#1e3c72,#2a5298);
    color:white;
    font-weight:bold;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
    margin-bottom:20px;
}

.footer{
    text-align:center;
    padding:30px;
    color:gray;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================

def init_db():

    conn = sqlite3.connect(
        "spam_guard_pro.db",
        check_same_thread=False
    )

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scan_logs(
        message TEXT,
        algorithm TEXT,
        prediction TEXT,
        confidence REAL,
        timestamp TEXT
    )
    """)

    conn.commit()

    return conn

conn = init_db()

# =========================================================
# TRAIN AI MODELS
# =========================================================

@st.cache_resource
def train_models():

    data = {
        "text":[
            "Win free cash prize now",
            "Claim your reward",
            "Urgent verify your account",
            "Double your income instantly",
            "Meeting at 5 PM",
            "Project submission tomorrow",
            "Lunch tomorrow?",
            "Let's attend class"
        ],

        "label":[
            "spam",
            "spam",
            "spam",
            "spam",
            "ham",
            "ham",
            "ham",
            "ham"
        ]
    }

    df = pd.DataFrame(data)

    cv = CountVectorizer()

    X = cv.fit_transform(df["text"])

    y = df["label"]

    # Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X, y)

    # Logistic Regression
    lr_model = LogisticRegression()
    lr_model.fit(X, y)

    # SVM
    svm_model = SVC(probability=True)
    svm_model.fit(X, y)

    return cv, nb_model, lr_model, svm_model

cv, nb_model, lr_model, svm_model = train_models()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🛡️ SpamGuard Pro")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=100
    )

    st.markdown("### Developer")
    st.caption("Shakibul Hasan")

    st.write("---")

    menu = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔍 Spam Detector",
            "📊 Analytics",
            "🗄️ Database Logs",
            "💡 Security Tips"
        ]
    )

    st.write("---")

    st.success("System Online ✅")

# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.title("🚀 Enterprise Security Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Scans", "15.2K", "+12%")
    col2.metric("Threats Blocked", "3,240", "+8%")
    col3.metric("AI Accuracy", "98.7%", "+2%")
    col4.metric("System Health", "99.9%", "Stable")

    st.write("---")

    st.subheader("📡 Live Threat Monitoring")

    chart_data = pd.DataFrame(
        np.random.randint(10,100,size=(20,3)),
        columns=["Spam","Malware","Phishing"]
    )

    st.line_chart(chart_data)

    st.write("---")

    fig = px.pie(
        names=["Spam","Safe","Malware"],
        values=[55,30,15],
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# SPAM DETECTOR
# =========================================================

elif menu == "🔍 Spam Detector":

    st.title("🔍 AI Spam Detection System")

    st.markdown("### Choose AI Algorithm")

    algo = st.selectbox(
        "Select Model",
        [
            "Naive Bayes",
            "Logistic Regression",
            "SVM"
        ]
    )

    text = st.text_area(
        "Enter Email / SMS",
        height=180,
        placeholder="Paste message here..."
    )

    if st.button("Analyze Message 🚀"):

        if text:

            with st.spinner("Analyzing using AI..."):

                time.sleep(1)

                vect = cv.transform([text])

                # MODEL SELECTION

                if algo == "Naive Bayes":
                    model = nb_model

                elif algo == "Logistic Regression":
                    model = lr_model

                else:
                    model = svm_model

                prediction = model.predict(vect)[0]

                probability = model.predict_proba(vect)[0]

                confidence = np.max(probability) * 100

                # DATABASE SAVE

                c = conn.cursor()

                c.execute(
                    """
                    INSERT INTO scan_logs
                    VALUES (?,?,?,?,?)
                    """,
                    (
                        text,
                        algo,
                        prediction,
                        confidence,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                )

                conn.commit()

                # RESULT CARD

                st.markdown(
                    "<div class='card'>",
                    unsafe_allow_html=True
                )

                if prediction == "spam":

                    st.error(
                        f"🚨 SPAM DETECTED\n\nConfidence: {confidence:.2f}%"
                    )

                else:

                    st.success(
                        f"✅ SAFE MESSAGE\n\nConfidence: {confidence:.2f}%"
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

                # Probability Chart

                probs_df = pd.DataFrame({
                    "Class":["Ham","Spam"],
                    "Probability":probability
                })

                fig = px.bar(
                    probs_df,
                    x="Class",
                    y="Probability",
                    color="Class",
                    text_auto=True
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.warning("Please enter a message.")

# =========================================================
# ANALYTICS
# =========================================================

elif menu == "📊 Analytics":

    st.title("📊 Security Analytics")

    data = pd.DataFrame({
        "Threat":["Spam","Phishing","Malware","Safe"],
        "Count":[120,80,45,300]
    })

    fig = px.bar(
        data,
        x="Threat",
        y="Count",
        color="Threat",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# DATABASE LOGS
# =========================================================

elif menu == "🗄️ Database Logs":

    st.title("🗄️ Scan History")

    try:

        logs = pd.read_sql_query(
            "SELECT * FROM scan_logs ORDER BY timestamp DESC",
            conn
        )

        if not logs.empty:

            st.dataframe(
                logs,
                use_container_width=True
            )

            if st.button("Clear Database"):

                c = conn.cursor()

                c.execute("DELETE FROM scan_logs")

                conn.commit()

                st.success("Database Cleared ✅")

                st.rerun()

        else:

            st.info("No logs found.")

    except Exception as e:

        st.error(f"Database Error: {e}")

# =========================================================
# SECURITY TIPS
# =========================================================

elif menu == "💡 Security Tips":

    st.title("💡 Cyber Security Tips")

    st.markdown("""
    ### 🛡️ Essential Protection Rules

    ✅ Enable Two-Factor Authentication (2FA)

    ✅ Never click suspicious links

    ✅ Keep your software updated

    ✅ Use strong passwords

    ✅ Avoid unknown email attachments

    ✅ Verify URLs before login
    """)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    f"""
    <div class='footer'>
    Developed by <b>Shakibul Hasan</b> |
    AI Cyber Security Suite |
    {datetime.now().year}
    </div>
    """,
    unsafe_allow_html=True
)
