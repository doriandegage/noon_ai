from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ✅ Load API Key from Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Ensure API Key is Set
if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OpenAI API Key! Set it in Render's environment variables.")

# ✅ OpenAI Client Initialization
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Noon AI is live on port 5050!"})

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # ✅ OpenAI Chat API Request
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an ecological strategist assistant."},
                      {"role": "user", "content": user_message}]
        )

        # ✅ Return AI Response
        return jsonify({"response": response.choices[0].message["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run Flask App on Port 5050
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # ✅ Sticking to 5050
    app.run(host="0.0.0.0", port=port, debug=True)
