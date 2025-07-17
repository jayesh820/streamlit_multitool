import streamlit as st
import datetime
import math
import cv2
import numpy as np
from PIL import Image
import requests

# ----------------- Functionalities ---------------------

def calculator():
    st.subheader("🔢 Simple Calculator")
    num1 = st.number_input("Enter first number")
    op = st.selectbox("Select operation", ['+', '-', '*', '/'])
    num2 = st.number_input("Enter second number")

    if st.button("Calculate"):
        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                st.error("Division by zero is not allowed.")
                return
        st.success(f"Result: {result:.2f}")


def currency_converter():
    st.subheader("💱 Currency Converter (INR to other)")
    amount = st.number_input("Enter amount in INR", min_value=0.0)
    currency = st.selectbox("Convert to", ["USD", "EUR", "GBP"])

    rates = {"USD": 0.012, "EUR": 0.011, "GBP": 0.0095}

    if st.button("Convert"):
        converted = amount * rates[currency]
        st.success(f"{amount} INR = {converted:.2f} {currency}")


def bmi_checker():
    st.subheader("⚖️ BMI Calculator")
    weight = st.number_input("Enter weight (kg)", min_value=1.0)
    height = st.number_input("Enter height (meters)", min_value=0.1)

    if st.button("Check BMI"):
        bmi = weight / (height ** 2)
        st.info(f"Your BMI is: {bmi:.2f}")
        if bmi < 18.5:
            st.warning("Category: Underweight")
        elif 18.5 <= bmi < 24.9:
            st.success("Category: Normal weight")
        elif 25 <= bmi < 29.9:
            st.warning("Category: Overweight")
        else:
            st.error("Category: Obese")


def age_calculator():
    st.subheader("📆 Age Calculator")
    birth_date = st.date_input("Enter your birth date")

    if st.button("Calculate Age"):
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        st.success(f"You are {age} years old.")


def emi_calculator():
    st.subheader("💸 Loan EMI Calculator")
    principal = st.number_input("Enter loan amount (₹)", min_value=0.0)
    rate = st.number_input("Annual interest rate (%)", min_value=0.0)
    tenure = st.number_input("Tenure in months", min_value=1)

    if st.button("Calculate EMI"):
        monthly_rate = rate / (12 * 100)
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure) / ((1 + monthly_rate) ** tenure - 1)
        total_payment = emi * tenure
        st.success(f"Monthly EMI: ₹{emi:.2f}")
        st.info(f"Total payment: ₹{total_payment:.2f}")


def weather_info():
    st.subheader("🌤️ Weather Info")
    city = st.text_input("Enter city name")

    if st.button("Get Weather"):
        api_key = "https://api.weatherapi.com/v1/current.json?key=demo&q="  # Use your own key for production
        try:
            response = requests.get(f"{api_key}{city}")
            data = response.json()
            if "error" in data:
                st.error(data["error"]["message"])
            else:
                temp_c = data["current"]["temp_c"]
                condition = data["current"]["condition"]["text"]
                humidity = data["current"]["humidity"]
                st.success(f"🌡️ Temp: {temp_c}°C\n💧 Humidity: {humidity}%\n⛅ Condition: {condition}")
        except Exception as e:
            st.error("Error fetching data. Check internet or API key.")


def image_to_sketch():
    st.subheader("🖼️ Image to Sketch Converter")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)

        img_array = np.array(image.convert("RGB"))
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)

        st.image(sketch, caption="Pencil Sketch", use_column_width=True)

# ---------------- Main App ---------------------

st.set_page_config(page_title="All-in-One Streamlit Tool", layout="centered")
st.title("🛠️ All-in-One Streamlit Tool")
st.write("Choose a tool from the sidebar 👇")

menu = st.sidebar.selectbox("Select Tool", [
    "Simple Calculator",
    "Currency Converter",
    "BMI Checker",
    "Age Calculator",
    "Loan EMI Calculator",
    "Weather Info",
    "Image to Sketch Converter"
])

if menu == "Simple Calculator":
    calculator()
elif menu == "Currency Converter":
    currency_converter()
elif menu == "BMI Checker":
    bmi_checker()
elif menu == "Age Calculator":
    age_calculator()
elif menu == "Loan EMI Calculator":
    emi_calculator()
elif menu == "Weather Info":
    weather_info()
elif menu == "Image to Sketch Converter":
    image_to_sketch()
