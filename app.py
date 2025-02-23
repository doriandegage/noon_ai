import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

# Weather.gov API requires a User-Agent (not an API key)
USER_AGENT = "(your-website.com, your-email@example.com)"  # Update this with your domain or email

# Homepage Route
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live with advanced eco-strategy features!"})

# Weather Route
@app.route("/weather", methods=["GET"])
def get_weather():
    location = "Austin, TX"  # Change this or make it dynamic
    weather_url = "https://api.weather.gov/gridpoints/EWX/158,89/forecast"  # Example for Austin, TX

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    try:
        response = requests.get(weather_url, headers=headers)
        response.raise_for_status()
        weather_data = response.json()
        forecast = weather_data["properties"]["periods"][0]["detailedForecast"]

        return jsonify({"response": f"🌦️ {forecast}"})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# AI Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Special Command Routing
        if "weather" in user_message:
            return get_weather()

        # Call OpenAI GPT-4 for AI-generated responses
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
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
