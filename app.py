from flask import Flask, request, jsonify, session
from flask_session import Session
import os

# Initialize Flask app
app = Flask(__name__)

# Enable session storage for conversation history
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Example predefined ecological strategies
ECOLOGICAL_STRATEGIES = {
    "rainwater harvesting": "Rainwater can be collected using bioswales, permeable surfaces, and storage tanks.",
    "soil regeneration": "Using compost, cover crops, and mycorrhizal fungi improves soil structure and fertility.",
    "native plant restoration": "Native plants require less water and support local wildlife while preventing soil erosion.",
    "solar irrigation": "Solar-powered pumps reduce dependency on fossil fuels for irrigation.",
    "biodiversity enhancement": "Creating microhabitats, planting pollinator-friendly species, and avoiding monoculture helps increase biodiversity."
}

@app.route("/ask", methods=["POST"])
def ask():
    """Handles chatbot queries related to ecological strategies."""
    data = request.get_json()
    user_message = data.get("message", "").lower()

    # Search for predefined strategies
    response = "I can assist with ecological strategies! What specific area are you focused on?"
    for key in ECOLOGICAL_STRATEGIES:
        if key in user_message:
            response = ECOLOGICAL_STRATEGIES[key]
            break

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
