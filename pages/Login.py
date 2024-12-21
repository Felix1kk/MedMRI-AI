
import streamlit as st
from firebase_config import authenticate_user

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



