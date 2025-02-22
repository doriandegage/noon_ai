from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load API Key from Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Set it in Render's environment variables.")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # ✅ Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an ecological strategist assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # ✅ Extract & return only the content (Fixing serialization issue)
        chat_response = response.choices[0].message.content

        return jsonify({"response": chat_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
