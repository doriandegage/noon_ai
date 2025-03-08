import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai  # Ensure this is installed

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Set up logging
logging.basicConfig(level=logging.INFO)

# Ensure Render uses port 5050
PORT = int(os.getenv("PORT", 5050))

# Load API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("Missing OpenAI API Key! Set it in Render's Environment Variables.")
    raise ValueError("OpenAI API Key is missing.")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Noon AI is running!"})

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required."}), 400

        # Generate AI response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_reply = response["choices"][0]["message"]["content"]

        return jsonify({"response": ai_reply})

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
