from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import openai
import os

# Use the new OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Noon AI is running."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json.get("message")
        if not user_input:
            return jsonify({"error": "No message provided."}), 400

        def generate():
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "system", "content": "You are an ecological strategist providing advice on sustainable solutions."},
                          {"role": "user", "content": user_input}],
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return Response(generate(), content_type="text/event-stream")

    except openai.OpenAIError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=10000)
