import requests
import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # <-- safe way
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.title("🌦 Simple Weather App")

city = st.text_input("Enter city name:")

if city:
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"📍 Weather in {city}, {data['sys']['country']}")
            st.metric("🌡 Temperature", f"{data['main']['temp']} °C")
            st.write(f"☁ Condition: {data['weather'][0]['description'].capitalize()}")
            st.write(f"💧 Humidity: {data['main']['humidity']}%")
            st.write(f"💨 Wind Speed: {data['wind']['speed']} m/s")

            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime("%H:%M:%S")
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime("%H:%M:%S")
            st.write(f"🌅 Sunrise: {sunrise}")
            st.write(f"🌇 Sunset: {sunset}")
        else:
            st.error("⚠️ City not found. Try another one!")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ No Internet Connection.")
