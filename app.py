from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ✅ Load API Key from Environment Variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Check if API key is set correctly
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Set it in Render's environment variables.")

# ✅ Initialize OpenAI client (Fix for OpenAI >= 1.0.0)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # ✅ OpenAI API Call (Updated for latest OpenAI versions)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an ecological strategist assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Start Flask Server with Render-Compatible Port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port, debug=True)
