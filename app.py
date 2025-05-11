import streamlit as st
import requests
import pandas as pd
import os


st.title("File Upload")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    if st.button("Confirm"):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post("http://127.0.0.1:8000/upload", files=files)
        if response.status_code == 200:
            st.write("File successfully uploaded!")
        #st.write("Backend response:", response.json())



st.title("Ask a Question")
with st.form("question", clear_on_submit=True, enter_to_submit=False):
    question = st.text_input("What is your question?")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(f"Question: {question}")
        with st.empty():
            st.write("Answer: loading....")
            response = requests.post("http://127.0.0.1:8000/ask", json={"question": question})
            if response.status_code == 200:
                st.write(f"Answer: {response.json()}")



st.title("Question Answer History")
if os.path.isfile("data/logs.txt"):
    df = pd.read_csv("data/logs.txt", delimiter=",")
    st.write(df)
