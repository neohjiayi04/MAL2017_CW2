from flask import abort, make_response, request, jsonify
from config import db
from models import Features, features_schema

def read_all():
    features = Features.query.all()
    return features_schema.dump(features)

def read_one(feature_id):
    feature = Features.query.get(feature_id)
    if not feature:
        abort(404)
    return jsonify({
        "feature_id": feature.feature_id,
        "feature_name": feature.feature_name
    })


def create():
    data = request.json
    new = Features(**data)
    db.session.add(new)
    db.session.commit()
    return jsonify({"message": "Feature created"}), 201


def update(feature_id):
    feature = Features.query.get(feature_id)
    if not feature:
        abort(404)
    data = request.json
    for key, value in data.items():
        setattr(feature, key, value)
    db.session.commit()
    return jsonify({"message": "Feature updated"})


def delete(feature_id):
    feature = Features.query.get(feature_id)
    if not feature:
        abort(404)
    db.session.delete(feature)
    db.session.commit()
    return "", 204
