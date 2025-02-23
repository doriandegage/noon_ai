import os
import requests
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load API Keys & Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_USER_AGENT = "hola@noon.eco"  # Your email for Weather.gov API requests
DEFAULT_LAT, DEFAULT_LON = 30.2672, -97.7431  # Austin, TX coordinates

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OpenAI API Key! Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live with eco strategy & weather updates!"})

@app.route("/status")
def status():
    return jsonify({"status": "🟢 Running", "port": os.environ.get("PORT", "5050")})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "❌ Message is required"}), 400

        # Handle Weather Requests
        if "weather" in user_message or "temperature" in user_message:
            city = "Austin, TX"
            lat, lon = DEFAULT_LAT, DEFAULT_LON

            # Fetch Weather Data from Weather.gov
            weather_url = f"https://api.weather.gov/points/{lat},{lon}"
            headers = {"User-Agent": WEATHER_USER_AGENT}

            try:
                point_response = requests.get(weather_url, headers=headers)
                point_response.raise_for_status()
                point_data = point_response.json()

                # Extract Forecast URL
                forecast_url = point_data["properties"]["forecast"]
                forecast_response = requests.get(forecast_url, headers=headers)
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()

                forecast = forecast_data["properties"]["periods"][0]["detailedForecast"]
                return jsonify({"response": f"🌤️ {city} Weather: {forecast}"})

            except requests.exceptions.RequestException as e:
                return jsonify({"response": f"⚠️ Weather data is unavailable: {str(e)}"})

        # Eco Strategy Responses
        eco_topics = {
            "solar irrigation": "🌞 Solar irrigation is an energy-efficient way to water crops using solar-powered pumps. Learn more at https://noon.eco/solar-irrigation",
            "rain harvesting": "💧 Rain harvesting captures and stores rainwater for later use. It helps reduce water bills and supports sustainability. Read more at https://noon.eco/rain-harvesting",
            "bioswales": "🌿 Bioswales help manage stormwater runoff, reducing flooding and improving water quality. Explore bioswale solutions at https://noon.eco/bioswales",
            "eco strategy": "🌍 Eco-strategies focus on sustainability, resource conservation, and environmental harmony. Ask about solar irrigation, rain harvesting, or bioswales!",
        }

        for key, response in eco_topics.items():
            if key in user_message:
                return jsonify({"response": response})

        # AI Chat Response with OpenAI
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
