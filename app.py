import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Enables frontend communication
import openai
import requests

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for your frontend
CORS(app, resources={r"/*": {"origins": "https://www.noon.eco"}})

# Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Optional for future weather integration

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set 'OPENAI_API_KEY' as an environment variable.")

openai.api_key = OPENAI_API_KEY

# Homepage Route (Basic Status Check)
@app.route("/")
def home():
    return jsonify({"message": "✅ Noon AI is live with full ecological chatbot functionality!"})

# Status Route (Useful for debugging)
@app.route("/status")
def status():
    return jsonify({
        "status": "🟢 Running",
        "port": os.environ.get("PORT", "5050"),
        "frontend": "https://www.noon.eco",
        "backend": "https://noon-ai.onrender.com"
    })

# AI Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Extract user message from JSON request
        data = request.json
        user_message = data.get("message", "").strip().lower()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # 🔹 Special Command Routing for Eco Strategies
        if user_message in ["schedule consultation", "book consultation"]:
            return jsonify({"response": "📅 Book a consultation here: https://www.noon.eco/consultation"})

        if user_message in ["recommend product", "shop", "store"]:
            return jsonify({"response": "🛒 Explore sustainable products here: https://www.noon.eco/products"})

        # 🔹 Eco Cognitive Accelerator – Direct Strategy Guidance
        eco_strategies = {
            "water management": "💧 Optimize your water usage and storage with advanced techniques. Learn more: https://www.noon.eco/water-management",
            "solar irrigation": "☀️ Use the power of the sun to enhance irrigation efficiency. Details here: https://www.noon.eco/solar-irrigation",
            "rain harvesting": "🌧️ Collect and store rainwater for sustainable use. Guide here: https://www.noon.eco/rain-harvesting",
            "bioswales": "🌿 Reduce runoff and naturally filter water with bioswales. Discover how: https://www.noon.eco/bioswales",
            "permaculture": "🌾 Design self-sustaining ecosystems using permaculture principles. Learn more: https://www.noon.eco/permaculture",
        }

        if user_message in eco_strategies:
            return jsonify({"response": eco_strategies[user_message]})

        # 🔹 Weather Integration (Future Support)
        if "weather" in user_message and WEATHER_API_KEY:
            location = "Austin, TX"  # Default location (expandable)
            weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
            weather_data = requests.get(weather_url).json()
            return jsonify({
                "response": f"🌤️ Current weather in {location}: {weather_data['current']['condition']['text']}, {weather_data['current']['temp_f']}°F"
            })

        # 🔹 Call OpenAI GPT-4 for Advanced AI Responses
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response.choices[0].message.content

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app on Render or locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Ensure correct port
    app.run(host="0.0.0.0", port=port)
