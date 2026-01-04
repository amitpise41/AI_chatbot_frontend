import streamlit as st
import requests

FASTAPI_BASE_URL = "http://localhost:8000"  # change if needed

def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter username and password")
            return

        try:
            resp = requests.post(
                f"{FASTAPI_BASE_URL}/token",
                data={
                    "username": username,
                    "password": password
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=10
            )

            if resp.status_code == 200:
                data = resp.json()

                st.session_state.token = data["access_token"]
                st.session_state.token_type = data.get("token_type", "bearer")
                st.session_state.username = username

                st.success("Login successful ✅")
                st.rerun()

            else:
                st.error(resp.json().get("detail", "Login failed"))

        except Exception as e:
            st.error(f"Error connecting to server: {e}")
