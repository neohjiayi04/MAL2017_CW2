from flask import jsonify
from models import Location, Route, Difficulty

def get_locations():
    items = Location.query.all()
    return jsonify([
        {
            "location_id": l.location_id,
            "location_name": l.location_name,
            "region": l.region,
            "country": l.country
        }
        for l in items
    ]), 200

def get_routes():
    items = Route.query.all()
    return jsonify([
        {"route_id": r.route_id, "route_type": r.route_type}
        for r in items
    ]), 200

def get_difficulties():
    items = Difficulty.query.all()
    return jsonify([
        {"difficulty_id": d.difficulty_id, "level": d.level}
        for d in items
    ]), 200


