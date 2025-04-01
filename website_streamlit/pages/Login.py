import streamlit as st
import re
import hashlib

class LoginPage:
    def __init__(self):
        st.set_page_config(page_title="Login", page_icon=":lock:")

    def validate_email(self, email):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def hash_password(self, password):
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login_form(self):
        """Create login form with validation"""
        st.markdown("""
        <style>
        .stTextInput label {
            color: var(--text-color) !important;
            opacity: 0.7;
        }
        .stTitle {
            color: var(--text-color) !important;
        }
        .stTextInput > div > div > input {
            color: var(--text-color) !important;
            background-color: var(--input-background) !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.title("🔐 Secure Login")
        col1, col2 = st.columns([1, 1])

        with col1:
            email = st.text_input("Email Address", placeholder="Enter your email")

            password = st.text_input("Password", type="password", placeholder="Enter your password")

        #with col2:


        login_btn = st.button("Log In", use_container_width=True)

        col_forgot, col_signup = st.columns(2)
        with col_forgot:
            st.markdown("[Forgot Password?](#)")
        with col_signup:
            st.markdown("[Sign Up](#)")

        if login_btn:
            if not email or not password:
                st.error("Please fill in all fields")
                return False

            if not self.validate_email(email):
                st.error("Invalid email format")
                return False

            if len(password) < 8:
                st.error("Password must be at least 8 characters")
                return False

            hashed_password = self.hash_password(password)
            st.success("Login Successful!")
            return True

        return False

    def run(self):
        """Main login page runner"""
        st.markdown("""
        <style>
        .stApp {
            background-color: var(--background-color);
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 1px solid var(--border-color);
            color: var(--text-color) !important;
        }
        a {
            color: var(--primary-color) !important;
        }
        </style>
        """, unsafe_allow_html=True)

        self.login_form()


def main():
    login_page = LoginPage()
    login_page.run()


main()