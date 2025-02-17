from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Noon AI, an ecological strategist and cognitive accelerator."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Ensure Flask listens on Render's port
    app.run(host="0.0.0.0", port=port, debug=True)
