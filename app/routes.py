from flask import Blueprint, jsonify, request
from .models import Observation
from . import db
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message":"Observation Log API is running 🚀"})

@main.route("/observations", methods = ["POST"])
def create_observation():
    data = request.get_json()

    required_fields = ["title", "category", "date"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
        
    try:
        observation = Observation(
            title=data["title"],
            category=data["category"],
            notes=data.get("notes"),
            duration_minutes=data.get("duration_minutes"),
            date=datetime.strptime(data["date"], "%Y-%m-%d").date()
        )

        db.session.add(observation)
        db.session.commit()
        db.session.refresh(observation)

        return jsonify({
            "id": observation.id,
            "title": observation.title,
            "category": observation.category,
            "notes": observation.notes,
            "duration_minutes": observation.duration_minutes,
            "date": observation.date.isoformat(),
            "created_at": observation.created_at.isoformat(),
            "message": "Observation created successfully"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    
@main.route("/observations", methods = ["GET"])
def get_observations():
    observations = Observation.query.all()

    result = []

    for obs in observations:
        result.append({
            "id": obs.id,
            "title": obs.title,
            "category": obs.category,
            "notes": obs.notes,
            "duration_minutes": obs.duration_minutes,
            "date": obs.date.isoformat(),
            "created_at": obs.created_at.isoformat()
        })

    return jsonify(result), 200

@main.route("/observations/<int:id>", methods = ["GET"])
def get_observations_by_id(id):
    observation = Observation.query.get(id)

    if not observation:
        return jsonify({"error":"Observation not found"}), 404
    
    return jsonify({
        "id": observation.id,
        "title": observation.title,
        "category": observation.category,
        "notes": observation.notes,
        "duration_minutes": observation.duration_minutes,
        "date": observation.date.isoformat(),
        "created_at": observation.created_at.isoformat()
    }), 200

@main.route("/observations/<int:id>", methods = ["DELETE"])
def delete_observations_by_id(id):
    observation = Observation.query.get(id)

    if not observation:
        return jsonify({"error":"Observation not found"}), 404
    
    db.session.delete(observation)
    db.session.commit()

    return jsonify({"message": f"Observation {id} deleted successfully"}), 200