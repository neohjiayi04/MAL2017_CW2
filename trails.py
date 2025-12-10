from flask import abort, make_response, request

from config import db
from models import Trails, trail_schema, trails_schema

def read_all():
    trails = Trails.query.all()
    return trails_schema.dump(trails)


def read_one(trail_id):
    trail = Trails.query.get(trail_id)
    if trail is None:
        abort(404)
    return trail_schema.dump(trail)


def create():
    data = request.json
    new_trail = Trails(**data)
    db.session.add(new_trail)
    db.session.commit()
    return {"message": "Trail created"}, 201


def update(trail_id):
    trail = Trails.query.get(trail_id)
    if trail is None:
        abort(404)

    data = request.json
    for key, value in data.items():
        setattr(trail, key, value)

    db.session.commit()
    return {"message": "Trail updated"}


def delete(trail_id):
    trail = Trails.query.get(trail_id)
    if trail is None:
        abort(404)

    db.session.delete(trail)
    db.session.commit()
    return "", 204
