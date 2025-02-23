import os
import openai
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Optional

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OpenAI API Key. Set 'OPENAI_API_KEY' in environment variables.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# === 🏠 Homepage Route ===
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live with eco-strategy chatbot!"})

# === 🔍 Status Check Route ===
@app.route("/status")
def status():
    return jsonify({"status": "🟢 Running", "port": os.environ.get("PORT", "5050")})

# === 💬 AI Chatbot Route ===
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # === 🌱 Special Eco-Related Commands ===
        eco_keywords = {
            "solar irrigation": "https://noon.eco/solar-irrigation",
            "rain harvesting": "https://noon.eco/rain-harvesting",
            "water management": "https://noon.eco/water-management",
            "bioswales": "https://noon.eco/bioswales"
        }
        for keyword, link in eco_keywords.items():
            if keyword in user_message:
                return jsonify({"response": f"🌿 Learn more about {keyword.title()} here: {link}"})

        # === ⛅ Weather API Integration (Optional) ===
        if "weather" in user_message and WEATHER_API_KEY:
            location = "Austin, TX"  # Default location
            weather_url = f"https://api.weather.gov/points/30.2672,-97.7431/forecast"
            headers = {"User-Agent": "noon.ai (your-email@example.com)"}  # Required for weather.gov API
            weather_data = requests.get(weather_url, headers=headers).json()

            try:
                forecast = weather_data['properties']['periods'][0]
                return jsonify({
                    "response": f"🌤️ {forecast['name']}: {forecast['detailedForecast']}"
                })
            except KeyError:
                return jsonify({"error": "⚠️ Unable to fetch weather data."}), 500

        # === 🤖 Call OpenAI GPT-4 API (Updated for v1.0+) ===
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 🚀 Run Flask App ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port)
