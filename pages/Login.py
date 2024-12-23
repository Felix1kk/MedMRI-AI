
import streamlit as st
from firebase_config import authenticate_user

st.set_page_config(
    page_title="Login",
    page_icon="☢️"
)

# Custom CSS to hide Streamlit icon, GitHub, and Fork icons
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {padding-top: 0;}
footer .stButton {display: none;}  /* Hide the Streamlit logo */
footer .stMetrics {display: none;}  /* Hide the Streamlit logo */
</style>
"""

# Inject custom CSS
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def login_page(cookies):
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user["username"]
            st.session_state["role"] = user["role"]
            st.session_state["page"] = "MainApp"
            st.session_state["user_id"] = user["id"]

            cookies["logged_in"] = str(True)
            cookies["current_page"] = "MainApp"
            cookies["user_id"] = user["id"]
            cookies.save()

            st.rerun()
        else:
            st.error("Invalid email or password")



