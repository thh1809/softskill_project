from flask import Blueprint, request, session, jsonify
from app.utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db()
    data = request.json
    if db.users.find_one({"username": data["username"]}):
        return jsonify({"error": "User exists"}), 400

    user = {
        "username": data["username"],
        "password": generate_password_hash(data["password"])
    }
    db.users.insert_one(user)
    return jsonify({"message": "User registered"})

@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db()
    data = request.json
    user = db.users.find_one({"username": data["username"]})

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user"] = str(user["_id"])
    session["username"] = user["username"]
    return jsonify({"message": "Login successful"})

@auth_bp.route("/profile", methods=["GET"])
def profile():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "user_id": session["user"],
        "username": session["username"]
    })
