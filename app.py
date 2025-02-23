import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Optional Weather API
USER_AGENT = "NoonEcoBot (noon.eco, contact@noon.eco)"  # Required for Weather API

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

# Setup logging
logging.basicConfig(level=logging.INFO)

# Homepage Route
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live with Eco Strategy features!"})

# Status Check Route
@app.route("/status")
def status():
    return jsonify({"status": "🟢 Running", "port": os.environ.get("PORT", "5050")})

# AI Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Special Command Routing
        if "schedule consultation" in user_message:
            return jsonify({"response": "📅 Book a consultation here: https://noon.eco/consultation"})

        if "recommend product" in user_message:
            return jsonify({"response": "🔍 Browse eco-friendly solutions here: https://noon.eco/products"})

        # Eco Cognitive Accelerator - Button Response
        if user_message in ["water management", "solar irrigation", "rain harvesting"]:
            return jsonify({
                "response": f"🌿 Learn more about {user_message.title()} here: https://noon.eco/{user_message.replace(' ', '-')}"
            })

        # **Weather API Integration**
        if "weather" in user_message and WEATHER_API_KEY:
            location = "Austin, TX"  # Default location (Update as needed)
            headers = {"User-Agent": USER_AGENT}
            weather_url = f"https://api.weather.gov/points/30.2672,-97.7431/forecast"
            weather_data = requests.get(weather_url, headers=headers).json()
            
            if "properties" in weather_data:
                forecast = weather_data["properties"]["periods"][0]["detailedForecast"]
                return jsonify({
                    "response": f"🌤️ Current forecast for {location}: {forecast}"
                })

        # **Call OpenAI GPT-4 for AI-generated responses**
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_response})

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run Flask app on Render or locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Render sets $PORT automatically
    app.run(host="0.0.0.0", port=port)
