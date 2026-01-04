import streamlit as st
from login_page import login_page
from chat_page import chat_page

st.set_page_config(
    page_title="Chat App",
    layout="centered"
)

def main():
    if "token" not in st.session_state:
        login_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()
