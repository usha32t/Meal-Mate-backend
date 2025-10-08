from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt

# Import blueprints
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.meal_routes import meal_bp
from routes.audio_routes import audio_bp
from routes.ai_routes import ai_bp

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py or environment
    app.config.from_object(Config)

    # Enable CORS for all domains on all routes (adjust origins for production)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints with URL prefixes
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(meal_bp, url_prefix="/api/meals")
    app.register_blueprint(audio_bp, url_prefix="/audio")
    app.register_blueprint(ai_bp, url_prefix="/ai")  # AI suggestions under /ai/suggestions

    return app

# Create the Flask app instance
app = create_app()
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Important: disable debug for production and avoid extra restarts
    app.run(host="0.0.0.0", port=port, debug=False)
