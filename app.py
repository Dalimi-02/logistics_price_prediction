import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, db
import pandas as pd
import altair as alt

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

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
def predict_price(distance, urgency, cargo_type, market_condition):
    # Dummy implementation for illustration
    return 100 + distance * 0.5 + urgency * 20

# CSV validation function
def validate_csv(df):
    required_columns = {"Price ($)", "Distance (km)", "Delivery Urgency (hours)", "Cargo Type", "Market Condition"}
    actual_columns = set(df.columns)
    return required_columns.issubset(actual_columns)

# Main app
def main():
    st.title("🚛 Logistics Price Prediction App")

    # Authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type='password', key="login_password")
            if st.button("Login"):
                login(email, password)

        with tab2:
            st.subheader("Sign Up")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type='password', key="signup_password")
            if st.button("Sign Up"):
                signup(email, password)
    else:
        st.sidebar.button("Logout", on_click=logout)

        # Main app content for authenticated users
        st.subheader("Predictive Model")

        # Upload CSV file
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)

            if not validate_csv(df):
                st.error("Uploaded CSV file does not have the required columns.")
            else:
                # Show data preview
                st.write("### Data Preview")
                st.dataframe(df.head())

                # Predictive Model Input
                st.subheader("Enter Prediction Parameters")
                distance = st.slider("Distance (km)", 0, 1000, 100)
                urgency = st.slider("Urgency (1-10)", 1, 10, 5)
                cargo_type = st.selectbox("Cargo Type", ["Perishable", "Non-Perishable"])
                market_condition = st.selectbox("Market Condition", ["High Demand", "Low Demand"])

                if st.button("Predict Price"):
                    price = predict_price(distance, urgency, cargo_type, market_condition)
                    st.write(f"### Estimated Price: ${price:.2f}")

                # Visualizations
                if not df.empty:
                    st.subheader("Visualizations")

                    # Distribution of Prices
                    st.subheader("Distribution of Prices")
                    price_chart = alt.Chart(df).mark_bar().encode(
                        alt.X("Price ($):Q", bin=True),
                        y='count()',
                    ).properties(width=600)
                    st.altair_chart(price_chart, use_container_width=True)

                    # Relationship between Distance and Price
                    st.subheader("Distance vs Price")
                    distance_price_chart = alt.Chart(df).mark_circle().encode(
                        x='Distance (km):Q',
                        y='Price ($):Q',
                        tooltip=['Distance (km)', 'Price ($)']
                    ).properties(width=600)
                    st.altair_chart(distance_price_chart, use_container_width=True)

                    # Relationship between Delivery Urgency and Price
                    st.subheader("Delivery Urgency vs Price")
                    urgency_price_chart = alt.Chart(df).mark_circle().encode(
                        x='Delivery Urgency (hours):Q',
                        y='Price ($):Q',
                        tooltip=['Delivery Urgency (hours)', 'Price ($)']
                    ).properties(width=600)
                    st.altair_chart(urgency_price_chart, use_container_width=True)

                    # Cargo Type vs Price (Pie Chart)
                    st.subheader("Cargo Type vs Price")
                    cargo_pie_chart = alt.Chart(df).mark_arc().encode(
                        theta=alt.Theta(field="Price ($)", type="quantitative", aggregate="sum"),
                        color=alt.Color(field="Cargo Type", type="nominal"),
                        tooltip=['Cargo Type', 'sum(Price ($))']
                    ).properties(width=600)
                    st.altair_chart(cargo_pie_chart, use_container_width=True)

                    # Market Condition Distribution (Pie Chart)
                    st.subheader("Market Condition Distribution")
                    market_condition_pie_chart = alt.Chart(df).mark_arc().encode(
                        theta=alt.Theta(field="Price ($)", type="quantitative", aggregate="sum"),
                        color=alt.Color(field="Market Condition", type="nominal"),
                        tooltip=['Market Condition', 'sum(Price ($))']
                    ).properties(width=600)
                    st.altair_chart(market_condition_pie_chart, use_container_width=True)

if __name__ == "__main__":
    main()
