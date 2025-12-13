from flask import request, jsonify
from models import db, Trail_Feature
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import random

def get_trail_features():
    trail_id = request.args.get("trail_id")
    q = Trail_Feature.query
    if trail_id:
        q = q.filter_by(trail_id=trail_id)
    items = q.all()

    result = [
        {
            "trail_feature_id": t.trail_feature_id,
            "trail_id": t.trail_id,
            "feature_id": t.feature_id
        }
        for t in items
    ]
    return jsonify(result), 200

def create_trail_feature(body):
    trail_id = body.get("trail_id")
    feature_id = body.get("feature_id")

    if not trail_id or not feature_id:
        return jsonify({"error": "trail_id and feature_id required"}), 400

    new_id = f"TF{random.randint(100000,999999)}"
    tf = Trail_Feature(trail_feature_id=new_id, trail_id=trail_id, feature_id=feature_id)

    try:
        db.session.add(tf)
        db.session.commit()
        return jsonify({"trail_feature_id": new_id, "trail_id": trail_id, "feature_id": feature_id}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error", "details": str(e.orig)}), 400

def delete_trail_feature(trail_feature_id):
    tf = Trail_Feature.query.get(trail_feature_id)
    if not tf:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(tf)
    db.session.commit()
    return '', 204
