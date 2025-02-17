import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
from flask_cors import CORS  # ✅ Added CORS for website integration

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # ✅ Enables cross-origin requests so Noon.Eco can access the API

@app.route('/')
def home():
    return "Noon AI is Live! Send a POST request to /ask"

@app.route('/ask', methods=['POST'])
def ask_noon_ai():
    """Handles incoming requests to interact with Noon AI."""
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.chat.completions.create(  # ✅ Updated to match OpenAI API v1+
            model="gpt-3.5-turbo",  # ✅ Using GPT-3.5 for faster response times
            messages=[
                {"role": "system", "content": "You are Noon AI, an ecological strategist and cognitive accelerator."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"response": response.choices[0].message.content})  # ✅ Correct response format

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # ✅ Ensures Flask runs on Render’s assigned port
    app.run(host="0.0.0.0", port=port, debug=True)
