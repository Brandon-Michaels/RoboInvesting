import streamlit as st
import requests

BACKEND_URL = "http://localhost:8080/api/chat"

st.title("Chatbot Interface")
st.markdown("Ask our AI-powered advisor anything about your finances:")

user_message = st.text_input("Your Message", "")

if st.button("Send"):
    if user_message.strip():
        try:
            response = requests.post(BACKEND_URL, json={"message": user_message})
            if response.status_code == 200:
                data = response.json()
                reply = data.get("reply", "No reply received.")
                st.markdown("### Chatbot Reply:")
                st.write(reply)
            else:
                st.error(f"Backend error: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a message.")
