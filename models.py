from extensions import db
from datetime import datetime

# ✅ User model
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    calorie_goal = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)   # height in cm (if using float)
    weight = db.Column(db.Float, nullable=True)   # weight in kg

    # Relationship to Meal model
    meals = db.relationship("Meal", backref="user", lazy=True)


# ✅ Meal model
class Meal(db.Model):
    __tablename__ = "meal"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., Breakfast, Lunch
    calories = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Optional macronutrients
    carbs = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)

    # Optional notes and audio URL
    note = db.Column(db.Text, nullable=True)
    audio_url = db.Column(db.String(255), nullable=True)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

