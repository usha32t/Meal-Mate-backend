from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)

# ✅ Register route
@user_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password=hashed_pw,
        name=data.get('name', ''),
        age=data.get('age'),
        height=data.get('height'),
        weight=data.get('weight'),
        calorie_goal=data.get('calorie_goal')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# ✅ Login route
@user_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401

# ✅ Get profile
@user_bp.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    profile_data = {
        "name": user.name,
        "calorie_goal": user.calorie_goal,
        "age": user.age,
        "height": user.height,
        "weight": user.weight,
        "email": user.email
    }
    return jsonify(profile_data), 200

# ✅ Update profile
@user_bp.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.calorie_goal = data.get('calorie_goal', user.calorie_goal)
    user.age = data.get('age', user.age)
    user.height = data.get('height', user.height)
    user.weight = data.get('weight', user.weight)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200
