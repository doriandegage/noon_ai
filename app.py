import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)  # Fix CORS issues for Noon.eco integration

# ✅ Load API Keys from Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Optional

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

# ✅ Homepage Route (For Testing)
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI Chatbot is Live!"})

# ✅ Status Route
@app.route("/status")
def status():
    return jsonify({"status": "🟢 Running", "port": os.environ.get("PORT", "5050")})

# ✅ AI Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # ✅ Special Command Routing (Fast Responses)
        if "schedule consultation" in user_message:
            return jsonify({"response": "📅 Book a consultation here: https://noon.eco/consultation"})

        if "recommend product" in user_message:
            return jsonify({"response": "🔍 Browse eco-friendly solutions here: https://noon.eco/products"})

        # ✅ Eco Cognitive Accelerator (Ecological Topics)
        eco_topics = {
            "solar irrigation": "https://noon.eco/solar-irrigation",
            "rain harvesting": "https://noon.eco/rain-harvesting",
            "bioswales": "https://noon.eco/bioswales",
            "eco restoration": "https://noon.eco/eco-restoration"
        }
        for topic, link in eco_topics.items():
            if topic in user_message:
                return jsonify({"response": f"🌱 Learn more about {topic.title()} here: {link}"})

        # ✅ Weather Integration (Optional)
        if "weather" in user_message and WEATHER_API_KEY:
            location = "Austin, TX"  # Default location (can customize per user)
            headers = {"User-Agent": "(noon.eco, contact@noon.eco)"}
            weather_url = f"https://api.weather.gov/points/30.2672,-97.7431/forecast"
            response = requests.get(weather_url, headers=headers)
            
            if response.status_code == 200:
                weather_data = response.json()
                forecast = weather_data["properties"]["periods"][0]["detailedForecast"]
                return jsonify({"response": f"🌤️ Current weather in {location}: {forecast}"})
            else:
                return jsonify({"error": "Failed to retrieve weather data"}), 500

        # ✅ OpenAI GPT-4 Response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_response = response["choices"][0]["message"]["content"]
        
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run Flask app on Render (or locally)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Render sets $PORT automatically
    app.run(host="0.0.0.0", port=port)
