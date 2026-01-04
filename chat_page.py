import streamlit as st
import requests

FASTAPI_BASE_URL = "http://localhost:8000"


def get_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


def load_chat_threads():
    resp = requests.get(
        f"{FASTAPI_BASE_URL}/chats",
        headers=get_headers()
    )
    resp.raise_for_status()
    return resp.json()


def load_chat_messages(thread_id):
    resp = requests.get(
        f"{FASTAPI_BASE_URL}/chats/{thread_id}",
        headers=get_headers()
    )
    resp.raise_for_status()
    return resp.json()


def create_new_chat():
    resp = requests.post(
        f"{FASTAPI_BASE_URL}/chats",
        headers=get_headers()
    )
    resp.raise_for_status()
    print(resp)
    return resp.json()["thread_id"]


def chat_page():
    st.title("🤗 How can I help you?")
    st.caption(f"Logged in as **{st.session_state.username}**")

    # -------------------------------
    # Sidebar: Chat history
    # -------------------------------
    with st.sidebar:
        st.header("💬 Chats")

        if st.button("➕ New Chat"):
            thread_id = create_new_chat()
            st.session_state.thread_id = thread_id
            st.session_state.messages = []
            st.rerun()

        try:
            chats = load_chat_threads()
        except Exception as e:
            st.error("Failed to load chats")
            return

        for thread_id in chats:
            if st.button(f"Chat {thread_id[:8]}", key=thread_id):
                st.session_state.thread_id = thread_id
                st.session_state.messages = load_chat_messages(thread_id)
                st.rerun()


    # -------------------------------
    # Require active chat
    # -------------------------------
    if "thread_id" not in st.session_state:
        st.info("Select or create a chat to start")
        return

    # -------------------------------
    # Render messages
    # -------------------------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # -------------------------------
    # Chat input
    # -------------------------------
    prompt = st.chat_input("Type your message...")

    if prompt:
        # Show user message immediately
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Send to backend
        resp = requests.post(
            f"{FASTAPI_BASE_URL}/chats/{st.session_state.thread_id}",
            json={
                "user_input": prompt
            },
            headers=get_headers()
        )

        resp.raise_for_status()
        assistant_reply = resp.json()["message"]

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        with st.chat_message("assistant"):
            st.markdown(assistant_reply["content"])

    st.divider()

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
