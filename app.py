import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import pandas as pd
import altair as alt
import json

# Initialize Firebase
if not firebase_admin._apps:
    try:
        firebase_key = {
            "type": st.secrets["firebase_key"]["type"],
            "project_id": st.secrets["firebase_key"]["project_id"],
            "private_key_id": st.secrets["firebase_key"]["private_key_id"],
            "private_key": st.secrets["firebase_key"]["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["firebase_key"]["client_email"],
            "client_id": st.secrets["firebase_key"]["client_id"],
            "auth_uri": st.secrets["firebase_key"]["auth_uri"],
            "token_uri": st.secrets["firebase_key"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase_key"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase_key"]["client_x509_cert_url"],
            "universe_domain": st.secrets["firebase_key"]["universe_domain"]
        }
        cred = credentials.Certificate(firebase_key)
        firebase_admin.initialize_app(cred)
        st.success("Firebase Initialized")
    except Exception as e:
        st.error(f"Error initializing Firebase: {str(e)}")

# Set page config
st.set_page_config(page_title="Logistics Price Prediction", page_icon="🚛")

# Authentication functions
def signup(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success("Sign up successful!")
        return user
    except Exception as e:
        st.error(f"Sign up failed: {str(e)}")
        return None

def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        # Note: In a real app, you'd verify the password here
        st.session_state.user = user
        st.session_state.authenticated = True
        st.success("Login successful!")
    except Exception as e:
        st.error(f"Login failed: {str(e)}")

def logout():
    st.session_state.user = None
    st.session_state.authenticated = False
    st.success("Logged out successfully!")

# Predictive model function (placeholder)
def predict_price(distance, urgency, cargo_type, market_conditions):
    return 1000  # Placeholder value

# UI elements
st.title("Logistics Price Prediction")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.header("Login")
    login_email = st.text_input("Email")
    login_password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(login_email, login_password)
    st.header("Sign Up")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        signup(signup_email, signup_password)
else:
    st.header("Price Prediction")
    distance = st.number_input("Distance (km)", min_value=0)
    urgency = st.selectbox("Delivery Urgency", ["Standard", "Express", "Overnight"])
    cargo_type = st.selectbox("Cargo Type", ["General", "Refrigerated", "Hazardous"])
    market_conditions = st.selectbox("Market Conditions", ["Stable", "Demand Surge", "Recession"])
    if st.button("Predict"):
        price = predict_price(distance, urgency, cargo_type, market_conditions)
        st.success(f"Estimated Price: ${price}")

    if st.button("Logout"):
        logout()
