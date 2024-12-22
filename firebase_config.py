
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import streamlit as st


# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"]["json_path"])
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to register a user
def register_user(email, username, password, role):
    existing_user = db.collection("users").where("email", "==", email).get()
    if existing_user:
        return {"success": False, "message": "Email already registered"}

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    registration_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_data = {
        "email": email,
        "username": username,
        "password": hashed_password,
        "role": role,
        "registration_time": registration_time,
        "last_login_time": None,
        "last_logout_time": None
    }
    db.collection("users").add(user_data)
    return {"success": True, "message": "User registered successfully"}

# Function to authenticate a user
def authenticate_user(email, password):
    users = db.collection("users").where("email", "==", email).get()
    for user in users:
        data = user.to_dict()
        if check_password_hash(data["password"], password):
            # Update last login timestamp
            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_ref = db.collection("users").document(user.id)
            user_ref.update({"last_login_time": login_time})
            data["id"] = user.id
            return data
    return None

# Function to update logout timestamp
def logout_user(user_id):
    try:
        logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_ref = db.collection("users").document(user_id)
        user_ref.update({"last_logout_time": logout_time})
    except Exception as e:
        print(f"Error updating logout time: {e}")



