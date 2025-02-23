import os
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

# === 🧠 AI Chatbot Route ===
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # === 🚀 Eco Strategy Responses ===
        eco_strategies = {
            "solar irrigation": "🌞 Learn more about Solar Irrigation here: https://noon.eco/solar-irrigation",
            "rain harvesting": "🌧️ Learn more about Rain Harvesting here: https://noon.eco/rain-harvesting",
            "water management": "🌊 Learn more about Water Management here: https://noon.eco/water-management"
        }
        for key, response in eco_strategies.items():
            if key in user_message:
                return jsonify({"response": response})

        # === ⛅ Weather API Integration ===
        if "weather" in user_message:
            try:
                location = "Austin, TX"  # Default location
                weather_url = f"https://api.weather.gov/points/30.2672,-97.7431/forecast"
                headers = {"User-Agent": "noon.ai (your-email@example.com)"}  # REQUIRED for weather.gov API
                
                # Fetch Weather Data
                weather_response = requests.get(weather_url, headers=headers)
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    forecast = weather_data['properties']['periods'][0]  # Get first forecast period

                    return jsonify({
                        "response": f"🌤️ {forecast['name']}: {forecast['detailedForecast']}"
                    })
                else:
                    return jsonify({"error": "⚠️ Weather API request failed."}), 500

            except Exception as e:
                return jsonify({"error": f"⚠️ Unable to fetch weather data: {str(e)}"}), 500

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
