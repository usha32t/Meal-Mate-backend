from flask import Blueprint, request, jsonify, current_app
import os
from extensions import db
audio_bp = Blueprint("audio", __name__)

@audio_bp.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename

    # Use current_app instead of app to avoid circular import
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)

    file.save(save_path)

    return jsonify({
        "message": "Audio uploaded successfully",
        "filename": filename
    }), 201