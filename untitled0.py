import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# টাইটেল এবং বর্ণনা
st.title("Email Spam Detector")
st.write("Enter a message to check if it's Spam or Not.")

# সিম্পল ট্রেনিং ডেটা
data = {
    'text': ['Free money now', 'Hi, how are you?', 'Claim prize', 'Meeting at 10am'],
    'label': ['spam', 'ham', 'spam', 'ham']
}
df = pd.DataFrame(data)

# ট্রেনিং প্রসেস
cv = CountVectorizer()
X = cv.fit_transform(df['text'])
model = MultinomialNB()
model.fit(X, df['label'])

# ইউজার ইনপুট
user_input = st.text_input("Message:")

if st.button("Predict"):
    if user_input:
        vect = cv.transform([user_input])
        prediction = model.predict(vect)
        st.success(f"This is a: {prediction[0].upper()}")
    else:
        st.warning("Please enter a message.")
