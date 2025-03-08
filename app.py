from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all requests

# ✅ Health Check Route (Ensures Render detects the service)
@app.route("/")
def home():
    return jsonify({"message": "Noon AI is running!"})

# ✅ Chatbot Route
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"].strip().lower()

    # ✅ Basic Ecological Response Logic
    responses = {
        "hello": "Hello! How can I assist you with ecological strategies?",
        "rainwater harvesting": "Rainwater can be collected using bioswales, permeable surfaces, and storage tanks.",
        "solar irrigation": "Solar irrigation uses solar-powered pumps to deliver water efficiently to plants.",
        "bioswales": "Bioswales help manage stormwater by filtering runoff and improving groundwater recharge."
    }

    # Find a matching response or return a default one
    response_text = responses.get(user_message, "I specialize in ecological strategies. What would you like to explore?")

    return jsonify({"response": response_text})

# ✅ Ensure the app runs on the correct port (Render uses $PORT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Default to 5050
    app.run(host="0.0.0.0", port=port)
