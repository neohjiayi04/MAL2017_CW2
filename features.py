from flask import request, jsonify
from models import db, Feature, feature_schema, features_schema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_features():
    items = Feature.query.all()
    return jsonify(features_schema.dump(items)), 200

def get_feature(feature_id):
    f = Feature.query.get(feature_id)
    if not f:
        return jsonify({"error": "Not found"}), 404
    return jsonify(feature_schema.dump(f)), 200

def create_feature(body):
    try:
        data = feature_schema.load(body)
        f = Feature(**data)
        db.session.add(f)
        db.session.commit()
        return jsonify(feature_schema.dump(f)), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error", "details": str(e.orig)}), 400

def update_feature(feature_id, body):
    f = Feature.query.get(feature_id)
    if not f:
        return jsonify({"error": "Not found"}), 404

    for key, value in body.items():
        if hasattr(f, key):
            setattr(f, key, value)

    db.session.commit()
    return jsonify(feature_schema.dump(f)), 200

def delete_feature(feature_id):
    f = Feature.query.get(feature_id)
    if not f:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(f)
    db.session.commit()
    return '', 204
