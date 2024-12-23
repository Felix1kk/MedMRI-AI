import streamlit as st
from firebase_config import register_user

def register_page(cookies):
    st.title("Register")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    role = st.selectbox("Role", ["User", "Admin"])

    if st.button("Register"):
        if password == confirm_password:
            result = register_user(email, username, password, role)
            if result["success"]:
                st.success("User registered successfully!")
                st.success(result["message"])

                st.session_state["page"] = "Login"
                cookies["current_page"] = "Login"
                cookies.save()

                st.rerun()
            else:
                st.error(result["message"])
        else:
            st.error("Passwords do not match")


