
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from firebase_config import logout_user

st.set_page_config(
    page_title="MedMRI AI",
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


firebase_api_key = st.secrets["firebase"]["api_key"]
firebase_password = st.secrets["firebase"]["password"]

# Initialize cookies
cookies = EncryptedCookieManager(
    prefix=firebase_api_key,
    password=firebase_password 
)
if not cookies.ready():
    st.stop()

# Load persistent state from cookies
logged_in = cookies.get("logged_in", "False") == "True"
current_page = cookies.get("current_page", "Login")
user_id = cookies.get("user_id")

# Sync session state with cookies
st.session_state["logged_in"] = st.session_state.get("logged_in", logged_in)
st.session_state["page"] = st.session_state.get("page", current_page)
st.session_state["user_id"] = st.session_state.get("user_id", user_id)

# Page routing
if st.session_state["page"] == "Login":
    from pages.Login import login_page
    login_page(cookies)
elif st.session_state["page"] == "Register":
    from pages.Register import register_page
    register_page(cookies)
elif st.session_state["page"] == "MainApp":
    from pages.MainApp import main_app
    main_app()

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    if st.session_state["page"] != "MainApp":
        if st.button("Go to Login"):
            st.session_state["page"] = "Login"
            cookies["current_page"] = "Login"
            cookies.save()
            st.rerun()
        if st.button("Go to Register"):
            st.session_state["page"] = "Register"
            cookies["current_page"] = "Register"
            cookies.save()
            st.rerun()
    else:
        if st.button("Logout"):
            # Ensure user logout logic is consistent
            if st.session_state.get("user_id"):
                logout_user(st.session_state["user_id"])  # Update the logout time (if applicable)
            cookies["logged_in"] = str(False)
            cookies["current_page"] = "Login"
            cookies["user_id"] = ""
            cookies.save()

            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]

            # Redirect to login page
            st.rerun()


