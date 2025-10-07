from flask import Blueprint, jsonify
from models import User, Meal
from extensions import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/stats", methods=["GET"])
def get_stats():
    try:
        user_count = db.session.query(User).count()
        meal_count = db.session.query(Meal).count()
        audio_note_count = db.session.query(Meal).filter(Meal.audio_url.isnot(None)).count()

        return jsonify({
            "users": user_count,
            "meals_logged": meal_count,
            "audio_notes": audio_note_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
