from flask import abort, make_response, request

from config import db
from models import TrailFeatures, trail_feature_schema, trail_features_schema

def read_all():
    links = TrailFeatures.query.all()
    return trail_features_schema.dump(links)


def read_one(trail_feature_id):
    link = TrailFeatures.query.get(trail_feature_id)
    if link is None:
        abort(404)
    return trail_feature_schema.dump(link)


def create():
    data = request.json
    new_link = TrailFeatures(**data)
    db.session.add(new_link)
    db.session.commit()
    return {"message": "Trail-Feature link created"}, 201


def update(trail_feature_id):
    link = TrailFeatures.query.get(trail_feature_id)
    if link is None:
        abort(404)

    data = request.json
    for key, value in data.items():
        setattr(link, key, value)

    db.session.commit()
    return {"message": "Trail-Feature link updated"}


def delete(trail_feature_id):
    link = TrailFeatures.query.get(trail_feature_id)
    if link is None:
        abort(404)

    db.session.delete(link)
    db.session.commit()
    return "", 204
