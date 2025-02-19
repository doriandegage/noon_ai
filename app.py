from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)
app.secret_key = "supersecretkey"  # Change this in production

# Simulated user database (for login system)
users = {}

@app.route('/')
def home():
    return "Noon AI is Live! Use /ask for questions, /login to log in."

@app.route('/ask', methods=['POST'])
def ask_noon_ai():
    """Handles user queries and provides responses."""
    data = request.json
    user_input = data.get("message")
    user_id = session.get("user_id", "guest")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Smart AI Response Paths
    response_text = None
    if "schedule" in user_input.lower():
        response_text = "I recommend booking a consultation. Click [here](https://calendly.com/noon-consult) to schedule."
    elif "product" in user_input.lower():
        response_text = "I suggest these products for your needs: [Solar Irrigation Kit](#), [Water Recycling System](#), [Eco-Friendly Soil Enhancer](#)."
    elif "not sure" in user_input.lower():
        response_text = "No worries! Let's start with a few questions to find your best ecological strategy."
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Noon AI, an ecological strategist and cognitive accelerator."},
                    {"role": "user", "content": user_input}
                ],
                stream=True  # Enables streaming responses
            )
            response_text = ""
            for chunk in response:
                response_text += chunk['choices'][0]['delta'].get('content', '')

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"response": response_text})

@app.route('/login', methods=['POST'])
def login():
    """Handles user login and profile creation."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if username in users and users[username] == password:
        session["user_id"] = username
        return jsonify({"message": f"Welcome back, {username}!"})
    
    users[username] = password
    session["user_id"] = username
    return jsonify({"message": f"Account created for {username}!"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
