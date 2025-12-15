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
