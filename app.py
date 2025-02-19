import openai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})  # ✅ Enable CORS for Squarespace

# ✅ Initialize OpenAI Client with API Key
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/ask', methods=['OPTIONS'])
def options():
    """Handles CORS preflight requests"""
    return '', 204

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        # ✅ Updated OpenAI API call (Fixed for latest version)
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an ecological strategist assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({"response": response.choices[0].message.content})

    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
