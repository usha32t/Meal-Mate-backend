from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Meal
from extensions import db
from datetime import datetime
from dateutil import parser  # Make sure it's installed: pip install python-dateutil

meal_bp = Blueprint("meals", __name__)

# ✅ Get all meals for the logged-in user
@meal_bp.route("", methods=["GET"])
@jwt_required()
def get_meals():
    user_id = get_jwt_identity()
    meals = Meal.query.filter_by(user_id=user_id).order_by(Meal.timestamp.desc()).all()

    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "category": m.category,
            "calories": m.calories,
            "quantity": m.quantity,
            "timestamp": m.timestamp.isoformat() if m.timestamp else None,
            "carbs": m.carbs,
            "protein": m.protein,
            "fat": m.fat,
            "note": m.note,
            "audio_url": m.audio_url
        } for m in meals
    ]), 200


# ✅ Log a new meal
@meal_bp.route("", methods=["POST"])
@jwt_required()
def log_meal():
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        timestamp = parser.isoparse(data["timestamp"]) if "timestamp" in data else datetime.utcnow()

        new_meal = Meal(
            name=data["name"],
            category=data["category"],
            calories=data["calories"],
            quantity=data.get("quantity", 1),
            carbs=data.get("carbs"),
            protein=data.get("protein"),
            fat=data.get("fat"),
            note=data.get("note"),
            timestamp=timestamp,
            user_id=user_id
        )

        db.session.add(new_meal)
        db.session.commit()

        return jsonify({"message": "Meal logged successfully."}), 201

    except Exception as e:
        print("Meal log error:", e)
        return jsonify({"error": str(e)}), 400


# ✅ Delete a meal
@meal_bp.route("/<int:meal_id>", methods=["DELETE"])
@jwt_required()
def delete_meal(meal_id):
    user_id = get_jwt_identity()
    meal = Meal.query.filter_by(id=meal_id, user_id=user_id).first()

    if not meal:
        return jsonify({"error": "Meal not found"}), 404

    try:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Meal deleted successfully."}), 200
    except Exception as e:
        print("Delete meal error:", e)
        return jsonify({"error": str(e)}), 500
