from flask import request, jsonify
from models import db, Trail, trail_schema, trails_schema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from sqlalchemy import text 

def get_trails():
    """Get all trails - simple version"""
    trails = Trail.query.all()
    return trails_schema.dump(trails), 200

def get_trails_detailed():
    """Get all trails with full details (location, difficulty, features, user info)"""
    try:
        query = text("SELECT * FROM CW2.vw_TrailDetails")
        result = db.session.execute(query)
        
        trails = []
        for row in result:
            trails.append({
                'trail_id': row.trail_id,
                'trail_name': row.trail_name,
                'description': row.description,
                'length': float(row.length) if row.length else None,
                'elevation_gain': row.elevation_gain,
                'estimated_time': float(row.estimated_time) if row.estimated_time else None,
                'visibility': row.visibility,
                'created_by': row.created_by,
                'created_by_name': row.created_by_name,
                'creator_email': row.creator_email,
                'created_at': row.created_at.isoformat() if row.created_at else None,
                'updated_at': row.updated_at.isoformat() if row.updated_at else None,
                'difficulty_level': row.difficulty_level,
                'location_name': row.location_name,
                'region': row.region,
                'country': row.country,
                'route_type': row.route_type,
                'features': row.features
            })
        
        return jsonify(trails), 200
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

def get_trail(trail_id):
    """Get single trail with full details"""
    try:
        query = text("SELECT * FROM CW2.vw_TrailDetails WHERE trail_id = :trail_id")
        result = db.session.execute(query, {"trail_id": trail_id})
        row = result.fetchone()
        
        if not row:
            return {"error": "Trail not found"}, 404
        
        trail = {
            'trail_id': row.trail_id,
            'trail_name': row.trail_name,
            'description': row.description,
            'length': float(row.length) if row.length else None,
            'elevation_gain': row.elevation_gain,
            'estimated_time': float(row.estimated_time) if row.estimated_time else None,
            'visibility': row.visibility,
            'created_by': row.created_by,
            'created_by_name': row.created_by_name,
            'creator_email': row.creator_email,
            'created_at': row.created_at.isoformat() if row.created_at else None,
            'updated_at': row.updated_at.isoformat() if row.updated_at else None,
            'difficulty_level': row.difficulty_level,
            'location_name': row.location_name,
            'region': row.region,
            'country': row.country,
            'route_type': row.route_type,
            'features': row.features
        }
        
        return jsonify(trail), 200
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

def create_trail(body):
    try:
        # Get the highest trail_id and generate next one
        last_trail = db.session.query(Trail).order_by(Trail.trail_id.desc()).first()
        
        if last_trail:
            last_num = int(last_trail.trail_id[1:])
            new_num = last_num + 1
        else:
            new_num = 1
        
        new_id = f"T{new_num:06d}"
        
        # Add trail_id and timestamps
        body['trail_id'] = new_id
        body['created_at'] = datetime.utcnow()
        body['updated_at'] = datetime.utcnow()
        
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

    # Update timestamp
    body['updated_at'] = datetime.utcnow()

    for key, value in body.items():
        if hasattr(trail, key) and key != 'trail_id' and key != 'created_at':
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