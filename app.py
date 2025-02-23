kimport os
import openai
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# === 🚀 Initialize Flask App ===
app = Flask(__name__)
CORS(app)  # Enables CORS for frontend

# === 🔑 Load API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")
openai.api_key = OPENAI_API_KEY

# === 🏡 Homepage Route ===
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live with Eco Strategy & Weather!"})

# === 🔥 Status Check Route ===
@app.route("/status")
def status():
    return jsonify({"status": "🟢 Running", "port": os.environ.get("PORT", "5050")})

# === 🌍 Function to Fetch Weather Data ===
def get_weather(city):
    try:
        # Convert city to latitude & longitude using OpenWeatherMap API (free signup needed)
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},US&limit=1&appid=YOUR_OPENWEATHER_API_KEY"
        geo_response = requests.get(geocode_url).json()

        if not geo_response:
            return "⚠️ City not found. Please try a different location."

        lat, lon = geo_response[0]['lat'], geo_response[0]['lon']

        # Get weather from weather.gov using lat/lon
        weather_url = f"https://api.weather.gov/points/{lat},{lon}/forecast"
        headers = {"User-Agent": "noon.ai (your-email@example.com)"}  # REQUIRED for weather.gov API

        weather_response = requests.get(weather_url, headers=headers)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            forecast = weather_data['properties']['periods'][0]  # Get first forecast period
            return f"🌤️ {forecast['name']} in {city}: {forecast['detailedForecast']}"
        else:
            return "⚠️ Weather data unavailable."

    except Exception as e:
        return f"⚠️ Error fetching weather data: {str(e)}"

# === 🧠 AI Chatbot Route ===
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # === 🌦️ Handle Weather Queries ===
        if "weather" in user_message:
            words = user_message.split()
            for word in words:
                if word.capitalize() not in ["Weather", "the", "in", "for", "is"]:
                    city = word.capitalize()
                    weather_info = get_weather(city)
                    return jsonify({"response": weather_info})

        # === 🚀 Eco Strategy Responses ===
        eco_strategies = {
            "solar irrigation": "🌞 Learn more about Solar Irrigation here: https://noon.eco/solar-irrigation",
            "rain harvesting": "🌧️ Learn more about Rain Harvesting here: https://noon.eco/rain-harvesting",
            "water management": "🌊 Learn more about Water Management here: https://noon.eco/water-management"
        }
        for key, response in eco_strategies.items():
            if key in user_message:
                return jsonify({"response": response})

        # === 🤖 OpenAI Chat Completion (v1 Fix) ===
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 🚀 Run Flask app on Render or locally ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Render sets $PORT automatically
    app.run(host="0.0.0.0", port=port)
