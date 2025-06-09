from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # For handling Cross-Origin Resource Sharing
import os
from gemini_chat import generate as generate_gemini_response # Renamed import for clarity

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, helpful for local development if frontend served differently

@app.route('/')
def index():
    """Serves the index.html file."""
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def handle_generate():
    """
    Handles POST requests to /generate.
    Expects JSON with a 'prompt_alpha' key.
    Calls the Gemini generate function and returns the response.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_prompt = data.get('prompt_alpha')

    if not user_prompt:
        return jsonify({"error": "Missing 'prompt_alpha' in request body"}), 400

    try:
        # Call the generate function from gemini_chat.py
        model_response = generate_gemini_response(user_prompt)
        return jsonify({"response": model_response})
    except Exception as e:
        print(f"An unexpected error occurred in /generate: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    # For local development, debug=True is helpful.
    # For production, debug should be False.
    # Host '0.0.0.0' makes it accessible externally (e.g., within a Docker container or local network).
    app.run(debug=True, host='0.0.0.0', port=3000)