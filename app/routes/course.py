from flask import Blueprint, request, jsonify
from app.utils.db import get_db
from bson import ObjectId
from app.middlewares import login_required
from app.utils.cache import redis_client, CACHE_TTL
import json

course_bp = Blueprint('courses', __name__)

@course_bp.route("/", methods=["GET"])
def get_courses():
    cache_key = "courses_list"
    cached = redis_client.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))
    db = get_db()
    courses = list(db.courses.find())
    for c in courses:
        c["_id"] = str(c["_id"])
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(courses))
    return jsonify(courses)

@course_bp.route("/", methods=["POST"])
@login_required
def create_course():
    db = get_db()
    data = request.json
    result = db.courses.insert_one(data)
    # Xóa cache khi thêm
    redis_client.delete("courses_list")
    return jsonify({"_id": str(result.inserted_id)}), 201

@course_bp.route("/<id>", methods=["PUT"])
@login_required
def update_course(id):
    db = get_db()
    data = request.json
    result = db.courses.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Course not found"}), 404
    # Xóa cache khi sửa
    redis_client.delete("courses_list")
    return jsonify({"message": "Course updated"})

@course_bp.route("/<id>", methods=["DELETE"])
@login_required
def delete_course(id):
    db = get_db()
    result = db.courses.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Course not found"}), 404
    # Xóa cache khi xóa
    redis_client.delete("courses_list")
    return jsonify({"message": "Course deleted"})
