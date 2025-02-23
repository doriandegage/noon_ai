import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import openai
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["https://www.noon.eco"])  # Allow requests from your website

# Load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Optional for weather integration

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

# Homepage Route
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live and running!"})

# Status Check Route
@app.route("/status")
def status():
    return jsonify({"status": "🟢 Running", "port": os.environ.get("PORT", "5050")})

# AI Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Special Commands
        if "schedule consultation" in user_message.lower():
            return jsonify({"response": "📅 Book a consultation here: https://noon.eco/consultation"})

        if "recommend product" in user_message.lower():
            return jsonify({"response": "🔍 Browse eco-friendly solutions here: https://noon.eco/products"})

        # Eco Cognitive Accelerator - Button Response
        if user_message.lower() in ["water management", "solar irrigation", "rain harvesting"]:
            return jsonify({
                "response": f"🌿 Learn more about {user_message.title()} here: https://noon.eco/{user_message.replace(' ', '-')}"
            })

        # Optional: Weather Integration
        if "weather" in user_message.lower() and WEATHER_API_KEY:
            location = "Austin, TX"  # Default location
            weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
            weather_data = requests.get(weather_url).json()
            return jsonify({
                "response": f"🌤️ Current weather in {location}: {weather_data['current']['condition']['text']}, {weather_data['current']['temp_f']}°F"
            })

        # Call OpenAI GPT-4 API for AI-generated responses
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app on Render or locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Render sets $PORT automatically
    app.run(host="0.0.0.0", port=port)
