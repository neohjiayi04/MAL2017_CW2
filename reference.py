from flask import jsonify
from models import Location, Route, Difficulty, Feature

def get_locations():
    """Get all available trail locations"""
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
    """Get all available route types"""
    items = Route.query.all()
    return jsonify([
        {"route_id": r.route_id, "route_type": r.route_type}
        for r in items
    ]), 200

def get_difficulties():
    """Get all difficulty levels"""
    items = Difficulty.query.all()
    return jsonify([
        {"difficulty_id": d.difficulty_id, "level": d.level}
        for d in items
    ]), 200

def get_features():
    """Get all available trail features"""
    items = Feature.query.all()
    return jsonify([
        {"feature_id": f.feature_id, "feature_name": f.feature_name}
        for f in items
    ]), 200