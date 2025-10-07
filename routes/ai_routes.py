from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

# Define the Blueprint
ai_bp = Blueprint('ai_routes', __name__)

@ai_bp.route('/suggestions', methods=['POST'])
@jwt_required()
def get_ai_suggestions():
    """
    AI Suggestion endpoint.
    Expects a JSON body with a 'meals' array.
    Returns mock suggestions or real API response (if configured).
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input
    if not data or "meals" not in data or not isinstance(data["meals"], list):
        return jsonify({"error": "Missing or invalid 'meals' in request body"}), 400

    try:
        # ✅ Return mock AI suggestions
        mock_suggestions = [
            "Add more fiber to your meals.",
            "Drink more water throughout the day.",
            "Include leafy greens in at least one meal."
        ]

        return jsonify({"suggestions": mock_suggestions}), 200

        # 🔁 Uncomment this section to use a real AI API in future
        # import requests
        # api_url = current_app.config.get("ZEMINI_API_URL")
        # api_key = current_app.config.get("ZEMINI_API_KEY")

        # if not api_url or not api_key:
        #     return jsonify({"error": "AI service configuration is missing"}), 500

        # headers = {
        #     "Authorization": f"Bearer {api_key}",
        #     "Content-Type": "application/json"
        # }

        # response = requests.post(
        #     f"{api_url}/suggest",
        #     json={"meals": data["meals"]},
        #     headers=headers,
        #     timeout=10
        # )

        # if response.status_code == 200:
        #     return jsonify(response.json())
        # else:
        #     logging.error(f"AI API error: {response.status_code} - {response.text}")
        #     return jsonify({"error": "Failed to get AI suggestions"}), response.status_code

    except Exception as e:
        logging.exception("Unexpected error in AI suggestion route")
        return jsonify({"error": "Internal server error"}), 500
