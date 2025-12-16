from flask import jsonify, request
from config import db
from models import Trail, Trail_Point, trail_schema, trails_schema, trail_points_schema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import text
from datetime import datetime


def get_trails():
    """Get all trails with basic information"""
    trails = Trail.query.all()
    return trails_schema.dump(trails), 200


def get_trails_detailed():
    """Get all trails with full details including related information"""
    try:
        query = text("SELECT * FROM CW2.vw_TrailDetails")
        result = db.session.execute(query)
        
        # ✅ FIX: Fetch all rows first before doing additional queries
        rows = result.fetchall()

        trails = []
        for row in rows:  # ✅ Changed from 'result' to 'rows'
            # Create trail data dictionary
            trail_data = {
                "trail_id": row.trail_id,
                "trail_name": row.trail_name,
                "description": row.description,
                "length": float(row.length) if row.length is not None else None,
                "elevation_gain": row.elevation_gain,
                "estimated_time": float(row.estimated_time) if row.estimated_time is not None else None,
                "visibility": row.visibility,
                "created_by": row.created_by,
                "created_by_name": row.created_by_name,
                "creator_email": row.creator_email,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                "difficulty_level": row.difficulty_level,
                "location_name": row.location_name,
                "region": row.region,
                "country": row.country,
                "route_type": row.route_type,
                "features": row.features
            }

            # ✅ Now safe to execute another query
            points = Trail_Point.query.filter_by(trail_id=row.trail_id)\
                                      .order_by(Trail_Point.sequence_no).all()
            trail_data["points"] = trail_points_schema.dump(points)
            
            trails.append(trail_data)

        return jsonify(trails), 200

    except Exception as e:
        return {"error": "Database error", "details": str(e)}, 500


def get_trail(trail_id):
    """Get a single trail with full details and GPS waypoints"""
    try:
        query = text(
            "SELECT * FROM CW2.vw_TrailDetails WHERE trail_id = :trail_id"
        )
        result = db.session.execute(query, {"trail_id": trail_id})
        row = result.fetchone()  # ✅ This is already correct - fetchone() closes the result

        if not row:
            return {"error": "Trail not found"}, 404

        # Create trail data dictionary
        trail = {
            "trail_id": row.trail_id,
            "trail_name": row.trail_name,
            "description": row.description,
            "length": float(row.length) if row.length is not None else None,
            "elevation_gain": row.elevation_gain,
            "estimated_time": float(row.estimated_time) if row.estimated_time is not None else None,
            "visibility": row.visibility,
            "created_by": row.created_by,
            "created_by_name": row.created_by_name,
            "creator_email": row.creator_email,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
            "difficulty_level": row.difficulty_level,
            "location_name": row.location_name,
            "region": row.region,
            "country": row.country,
            "route_type": row.route_type,
            "features": row.features
        }

        # ✅ Now safe to execute another query
        points = Trail_Point.query.filter_by(trail_id=trail_id)\
                                  .order_by(Trail_Point.sequence_no).all()
        trail["points"] = trail_points_schema.dump(points)
    
        return jsonify(trail), 200

    except Exception as e:
        return {"error": "Database error", "details": str(e)}, 500


def create_trail(body):
    """Create a new trail with metadata"""
    try:
        # Generate new trail ID
        last_trail = (
            db.session.query(Trail)
            .order_by(Trail.trail_id.desc())
            .first()
        )

        if last_trail:
            next_num = int(last_trail.trail_id[1:]) + 1
        else:
            next_num = 1

        trail_id = f"T{next_num:06d}"

        # Validate data with schema
        data = trail_schema.load(body)

        # Set timestamps
        now = datetime.utcnow().replace(microsecond=0)

        # Use raw SQL to insert (avoids pyodbc DECIMAL bug)
        query = text("""
            INSERT INTO CW2.Trail 
            (trail_id, trail_name, description, visibility, created_at, updated_at, 
             location_id, length, estimated_time, elevation_gain, route_id, difficulty_id, created_by)
            VALUES 
            (:trail_id, :trail_name, :description, :visibility, :created_at, :updated_at,
             :location_id, :length, :estimated_time, :elevation_gain, :route_id, :difficulty_id, :created_by)
        """)

        db.session.execute(query, {
            "trail_id": trail_id,
            "trail_name": data["trail_name"],
            "description": data.get("description"),
            "visibility": data["visibility"],
            "created_at": now,
            "updated_at": now,
            "location_id": data.get("location_id"),
            "length": float(data["length"]) if data.get("length") else None,
            "estimated_time": float(data["estimated_time"]) if data.get("estimated_time") else None,
            "elevation_gain": data.get("elevation_gain"),
            "route_id": data["route_id"],
            "difficulty_id": data["difficulty_id"],
            "created_by": data["created_by"]
        })

        db.session.commit()

        # Fetch the created trail to return
        created_trail = Trail.query.get(trail_id)
        return trail_schema.dump(created_trail), 201

    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Integrity error", "details": str(e.orig)}, 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500


def update_trail(trail_id, body):
    """Update an existing trail's metadata"""
    # Check if trail exists
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"error": "Trail not found"}, 404

    try:
        # Load and validate partial update
        data = trail_schema.load(body, partial=True)

        # Build dynamic UPDATE query
        update_fields = []
        params = {"trail_id": trail_id}

        for key, value in data.items():
            if key not in ("trail_id", "created_at", "points"):
                update_fields.append(f"{key} = :{key}")
                
                # Convert Decimal to float for numeric fields
                if key in ("length", "estimated_time") and value is not None:
                    params[key] = float(value)
                else:
                    params[key] = value

        # Always update timestamp
        update_fields.append("updated_at = :updated_at")
        params["updated_at"] = datetime.utcnow().replace(microsecond=0)

        # Execute raw SQL UPDATE
        query = text(f"""
            UPDATE CW2.Trail 
            SET {', '.join(update_fields)}
            WHERE trail_id = :trail_id
        """)

        db.session.execute(query, params)
        db.session.commit()

        # Fetch updated trail to return
        updated_trail = Trail.query.get(trail_id)
        return trail_schema.dump(updated_trail), 200

    except IntegrityError as e:
        db.session.rollback()
        return {"error": "Integrity error", "details": str(e.orig)}, 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500


def delete_trail(trail_id):
    """Delete a trail and its associated waypoints (cascade)"""
    trail = Trail.query.get(trail_id)
    if not trail:
        return {"error": "Trail not found"}, 404

    try:
        db.session.delete(trail)
        db.session.commit()
        return "", 204

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error", "details": str(e)}, 500