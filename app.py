from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# ✅ Load API Key from Environment Variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OpenAI API Key is missing! Set it in Render's Environment Variables.")

# ✅ OpenAI Client
openai.api_key = OPENAI_API_KEY

# ✅ Health Check Route (Prevents 404 Errors)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Noon AI is running!"})

# ✅ Chatbot Route
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "No message provided!"}), 400

        # ✅ Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an ecological strategist AI."},
                      {"role": "user", "content": user_message}]
        )

        ai_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run App on Port 5050
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
