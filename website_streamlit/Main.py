import streamlit as st

st.set_page_config(page_title="RoboInvest", layout="wide")

hide_streamlit_style = """
            <style>
            /* Hide the default Streamlit top menu */
            #MainMenu {visibility: hidden;}
            
            /* Hide the footer */
            footer {visibility: hidden;}
            
            /* Hide the Streamlit default page navigation in the sidebar */
            .css-1lcbmhc {display: none;}  /* Remove the default page selector in sidebar */
            
            /* Hide Streamlit's "Main" entry from the sidebar */
            .css-1f8f0p4 {display: none;}  /* Remove "Main" option from sidebar */
            
            /* Hide Streamlit's automatic navigation, leaving only custom dropdown */
            .css-1kyxreq {display: none;}  /* Hide the default sidebar components like pages list */
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

from pages import Home, Login, Chatbot, Learn, Assets

PAGES = {
    "Home": Home,
    "Login": Login,
    "Chatbot": Chatbot,
    "Learn": Learn,
    "Assets": Assets
}

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))

PAGES[selection].app()











