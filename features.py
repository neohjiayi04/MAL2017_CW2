from flask import request, jsonify
from config import db, ma
from models import Feature, feature_schema, features_schema
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
        # Get the highest feature_id and generate next one
        last_feature = db.session.query(Feature).order_by(Feature.feature_id.desc()).first()
        
        if last_feature:
            # Extract number from last ID (e.g., 'F000015' -> 15)
            last_num = int(last_feature.feature_id[1:])
            new_num = last_num + 1
        else:
            new_num = 1
        
        # Format as F000001, F000002, etc.
        new_id = f"F{new_num:06d}"
        
        # Add feature_id to the body
        body['feature_id'] = new_id
        
        data = feature_schema.load(body)
        f = Feature(**data)
        db.session.add(f)
        db.session.commit()
        return jsonify(feature_schema.dump(f)), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error", "details": str(e.orig)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

def update_feature(feature_id, body):
    f = Feature.query.get(feature_id)
    if not f:
        return jsonify({"error": "Not found"}), 404

    for key, value in body.items():
        if hasattr(f, key) and key != 'feature_id':
            setattr(f, key, value)

    try:
        db.session.commit()
        return jsonify(feature_schema.dump(f)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

def delete_feature(feature_id):
    f = Feature.query.get(feature_id)
    if not f:
        return jsonify({"error": "Not found"}), 404

    try:
        db.session.delete(f)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500