import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_USER_AGENT = "hola@noon.eco"  # Your email for Weather.gov API requests
DEFAULT_CITY = "Austin"

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
            return jsonify({"error": "Message is required"}), 400

        # Weather API Handling
        if "weather" in user_message:
            city = DEFAULT_CITY
            if "in" in user_message:
                parts = user_message.split("in")
                if len(parts) > 1:
                    city = parts[1].strip()

            weather_url = f"https://api.weather.gov/points/30.2672,-97.7431"  # Austin coordinates
            headers = {"User-Agent": WEATHER_USER_AGENT}

            try:
                response = requests.get(weather_url, headers=headers)
                response.raise_for_status()
                data = response.json()

                forecast_url = data["properties"]["forecast"]
                forecast_response = requests.get(forecast_url, headers=headers).json()
                forecast = forecast_response["properties"]["periods"][0]["detailedForecast"]

                return jsonify({"response": f"🌤️ {city} Weather: {forecast}"})
            except Exception as e:
                return jsonify({"error": f"Failed to fetch weather: {str(e)}"}), 500

        # Eco Strategy Responses
        eco_topics = {
            "solar irrigation": "🌞 Solar irrigation is an energy-efficient way to water crops using solar-powered pumps. Learn more at https://noon.eco/solar-irrigation",
            "rain harvesting": "💧 Rain harvesting captures and stores rainwater for later use. It helps reduce water bills and supports sustainability. Read more at https://noon.eco/rain-harvesting",
            "bioswales": "🌿 Bioswales help manage stormwater runoff, reducing flooding and improving water quality. Explore bioswale solutions at https://noon.eco/bioswales",
        }

        for key, response in eco_topics.items():
            if key in user_message:
                return jsonify({"response": response})

        return jsonify({"response": "I can provide insights on eco-strategies, water systems, and sustainable solutions. Ask me about solar irrigation, rain harvesting, or bioswales!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
