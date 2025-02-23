import os
import openai
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Not needed for weather.gov, just for future expansion

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

# ✅ Define Custom Eco Strategy Responses
ECO_STRATEGIES = {
    "solar irrigation": "Solar irrigation is an efficient method of using solar energy to power water pumps, reducing dependency on fossil fuels. Learn more at: https://noon.eco/solar-irrigation",
    "rain harvesting": "Rainwater harvesting involves collecting and storing rainwater for later use. This reduces water waste and is ideal for sustainable landscapes. Learn more at: https://noon.eco/rain-harvesting",
    "bioswales": "Bioswales are landscape elements designed to filter and slow down stormwater runoff, reducing erosion and improving water quality. More details: https://noon.eco/bioswales",
    "eco strategy": "An eco-strategy is a sustainable approach to managing resources efficiently. Noon Re'Genesis focuses on decentralized water, solar energy, and natural ecosystem integration."
}

# ✅ Homepage Route
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live and running!"})

# ✅ Status Check Route
@app.route("/status")
def status():
    return jsonify({"status": "🟢 Running", "port": os.environ.get("PORT", "5050")})

# ✅ Weather.gov API Integration
def get_weather(city):
    """Fetch weather data from weather.gov for a given city."""
    city_coordinates = {
        "austin": "30.2672,-97.7431",
        "san antonio": "29.4241,-98.4936",
        "houston": "29.7604,-95.3698",
        "dallas": "32.7767,-96.7970"
    }

    if city.lower() in city_coordinates:
        lat_lon = city_coordinates[city.lower()]
        weather_url = f"https://api.weather.gov/points/{lat_lon}/forecast"
        headers = {"User-Agent": "(noon.eco, support@noon.eco)"}  # Required by weather.gov API

        response = requests.get(weather_url, headers=headers)
        weather_data = response.json()

        if "properties" in weather_data and "periods" in weather_data["properties"]:
            forecast = weather_data["properties"]["periods"][0]
            return f"🌤️ {forecast['name']} in {city.title()}: {forecast['shortForecast']}, {forecast['temperature']}°F"
        else:
            return "⚠️ Weather data is unavailable at the moment."
    else:
        return "⚠️ Weather information for this location is not available."

# ✅ Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower().strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # 🌿 **Custom Eco Strategy Responses**
        for key in ECO_STRATEGIES:
            if key in user_message:
                return jsonify({"response": f"🌱 {ECO_STRATEGIES[key]}"})

        # 🌤️ **Weather.gov API Response**
        if "weather" in user_message:
            for city in ["austin", "san antonio", "houston", "dallas"]:
                if city in user_message:
                    return jsonify({"response": get_weather(city)})

            return jsonify({"response": "🌎 Please specify a city (Austin, San Antonio, Houston, Dallas) for the weather update."})

        # 🔥 **Fallback: OpenAI GPT-4 Response**
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run Flask App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Default Render port
    app.run(host="0.0.0.0", port=port)
