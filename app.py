from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ✅ Load API Key (Ensure this is set in Render's Environment Variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Set it in Render's environment variables.")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Root Route (Prevents 404 on Render)
@app.route("/")
def home():
    return "Noon AI is Running!"

# ✅ Handle AI Requests
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # ✅ OpenAI Chat Request
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an ecological strategist assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # ✅ Extract and return AI response
        ai_response = response.choices[0].message.content.strip()
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run App (Uses Render's Dynamic Port)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns this dynamically
    app.run(host="0.0.0.0", port=port, debug=True)
