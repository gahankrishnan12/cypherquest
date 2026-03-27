import streamlit as st

st.title("My Hackathon App 🚀")
st.write("Hello, world!")

name = st.text_input("Enter your name")
if st.button("Submit"):
    st.success(f"Hello, {name}!")