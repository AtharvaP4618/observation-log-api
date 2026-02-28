from flask import Blueprint, jsonify, request, abort 
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
            abort(400, description=f"{field} is required")
        
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

        return jsonify(observation.to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    
@main.route("/observations", methods = ["GET"])
def get_observations():
    category = request.args.get("category")
    date = request.args.get("date")
    min_duration = request.args.get("min_duration")
    max_duration = request.args.get("max_duration")

    query = Observation.query 
    if category:
        query = query.filter(Observation.category == category)

    if date:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(Observation.date == parsed_date)
        except ValueError:
            abort(400, description="Invalid date format. Use YYYY-MM-DD.")


    if min_duration:
        try:
            min_duration = int(min_duration)
            query = query.filter(
                Observation.duration_minutes >= min_duration
            )
        except ValueError:
            abort(400, description="min_duration must be an integer")

    if max_duration:
        try:
            max_duration = int(max_duration)
            query = query.filter(
                Observation.duration_minutes <= max_duration
            )
        except ValueError:
            abort(400, description="max_duration must be an integer")
    
    page = request.args.get("page", 1)
    limit = request.args.get("limit", 5)

    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        abort(400, description="page and limit must be integers")
    
    pagination = query.paginate(
        page = page,
        per_page = limit,
        error_out = False
    )

    observations = pagination.items

    return jsonify({
        "meta" : {
            "total": pagination.total,
            "page": page,
            "limit": limit,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        },
        "data": [obs.to_dict() for obs in observations] 
    }), 200


@main.route("/observations/<int:id>", methods = ["GET"])
def get_observations_by_id(id):
    observation = Observation.query.get(id)

    if not observation:
        abort(404, description="Observation not found")
    
    return jsonify(observation.to_dict()), 200

@main.route("/observations/<int:id>", methods = ["DELETE"])
def delete_observations_by_id(id):
    observation = Observation.query.get(id)

    if not observation:
        abort(404, description="Observation not found")
    
    db.session.delete(observation)
    db.session.commit()

    return jsonify({
        "message": "Observation deleted successfully"
    }), 200

@main.route("/observations/<int:id>", methods = ["PUT"])
def update_observation(id):
    observation = Observation.query.get(id)

    if not observation:
        abort(404, description="Observation not found")    
    
    data = request.get_json()

    if "title" in data:
        observation.title = data["title"]
    if "category" in data:
        observation.category = data["category"]
    if "notes" in data:
        observation.notes = data["notes"]
    if "duration_minutes" in data:
        observation.duration_minutes = data["duration_minutes"]
    if "date" in data:
        observation.date = datetime.strptime(
            data["date"], "%Y-%m-%d"
        ).date()

    db.session.commit()

    return jsonify(observation.to_dict()), 200  
                               