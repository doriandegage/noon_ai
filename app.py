import os
import openai
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow frontend requests

# === 🔑 Load API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Optional (Set it if using weather)
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

# === 🌎 Home Route ===
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live with eco-strategy support!"})

# === 💬 AI Chatbot Route ===
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # === 🌞 Eco Topics (Instant Responses) ===
        eco_topics = {
            "solar irrigation": "🌞 Learn more: https://noon.eco/solar-irrigation",
            "rain harvesting": "🌧️ Learn more: https://noon.eco/rain-harvesting",
            "water management": "💧 Learn more: https://noon.eco/water-management"
        }
        for topic, response in eco_topics.items():
            if topic in user_message:
                return jsonify({"response": response})

        # === 🌦️ Weather API Integration (Optional) ===
        if "weather" in user_message and WEATHER_API_KEY:
            location = "San Antonio"  # Default location (Modify as needed)
            weather_url = f"https://api.weather.gov/points/29.4241,-98.4936"
            headers = {"User-Agent": "NoonAI/1.0 (contact@noon.eco)"}
            response = requests.get(weather_url, headers=headers).json()

            # Get forecast URL from Weather.gov API
            forecast_url = response["properties"]["forecast"]
            forecast_data = requests.get(forecast_url, headers=headers).json()
            forecast = forecast_data["properties"]["periods"][0]["detailedForecast"]

            return jsonify({"response": f"🌤️ Weather in {location}: {forecast}"})

        # === 🤖 OpenAI AI Chat (Updated for v1 API) ===
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 🚀 Run Flask App ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5050)))
