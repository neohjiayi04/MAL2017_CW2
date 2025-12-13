from flask import request, jsonify
from models import db, Trail, trail_schema, trails_schema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def get_trails():
    trails = Trail.query.all()
    return trails_schema.dump(trails), 200

def get_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"error": "Trail not found"}, 404
    return (trail_schema.dump(trail)), 200

def create_trail(body):
    try:
        data = trail_schema.load(body)
        new_trail = Trail(**data)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Integrity error", "details": str(e.orig)}, 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500

def update_trail(trail_id, body):
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"error": "Trail not found"}, 404

    for key, value in body.items():
        if hasattr(trail, key):
            setattr(trail, key, value)

    try:
        db.session.commit()
        return trail_schema.dump(trail), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500

def delete_trail(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"error": "Trail not found"}, 404

    try:
        db.session.delete(trail)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500
