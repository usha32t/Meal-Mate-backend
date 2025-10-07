import os

class Config:
    # Enable Flask debug mode
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
        os.makedirs(INSTANCE_DIR, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'mealmate.sqlite')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask secret keys
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")

    # File upload configuration
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

    # Zemini AI configuration (Hardcoded)
    ZEMINI_API_KEY = "AIzaSyBI06B1uPPu0lv0LFbaHrmQoAEkuwMHas8"
    # config.py or app.py
    ZEMINI_API_URL = "https://mocki.io/v1/your-fake-endpoint-id"
