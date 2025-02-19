from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import openai
import json
import os

app = Flask(__name__)
CORS(app)

# OpenAI API Key (Ensure it's set in your environment variables)
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return "Noon AI is running!"

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        def generate():
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Noon AI, an ecological strategist. Provide structured responses with bullet points, numbered steps, or categories."},
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return Response(generate(), content_type="text/plain")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
