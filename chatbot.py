import openai
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for handling cross-origin requests

# Set your OpenAI API key here (ensure it's secure in production)
openai.api_key = "YOUR_OPENAI_API_KEY"


# Function to interact with OpenAI chat model
def get_chatbot_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7,  # Adjust temperature for creativity vs. coherence
        )
        return response.choices[0].message["content"]
    except Exception as e:
        raise Exception(f"Error fetching chatbot response: {str(e)}")


# Route to handle incoming chat messages
@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        message = data.get("message")
        if not message:
            return jsonify({"error": "Message is required"}), 400

        global messages
        user_message = {"role": "user", "content": message}
        assistant_message = {"role": "assistant", "content": ""}

        messages = [user_message]

        if len(messages) > 1:
            assistant_message = get_chatbot_response(messages)
            messages.append(assistant_message)

        return jsonify({"response": assistant_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
