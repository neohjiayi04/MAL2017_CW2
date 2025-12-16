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
        
        # Fetch all rows first before doing additional queries
        rows = result.fetchall()

        trails = []
        for row in rows:
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

            # Now safe to execute another query
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
        row = result.fetchone()

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

        # Now safe to execute another query
        points = Trail_Point.query.filter_by(trail_id=trail_id)\
                                  .order_by(Trail_Point.sequence_no).all()
        trail["points"] = trail_points_schema.dump(points)
    
        return jsonify(trail), 200

    except Exception as e:
        return {"error": "Database error", "details": str(e)}, 500


def create_trail(body):
    """Create a new trail with metadata and optional GPS waypoints"""
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

        # Separate points from trail data for validation
        points_data = body.pop("points", None)  # Extract points if present
        
        # Validate trail data with schema
        data = trail_schema.load(body)

        # Set timestamps
        now = datetime.utcnow().replace(microsecond=0)

        # Use raw SQL to insert trail (avoids pyodbc DECIMAL bug)
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

        # Handle trail points if provided
        if points_data and isinstance(points_data, list) and len(points_data) > 0:
            # Get last trail point ID to generate next IDs
            last_point = (
                db.session.query(Trail_Point)
                .order_by(Trail_Point.trail_point_id.desc())
                .first()
            )
            
            if last_point:
                next_point_num = int(last_point.trail_point_id[2:]) + 1
            else:
                next_point_num = 1

            # Insert each point
            for point in points_data:
                point_id = f"TP{next_point_num:06d}"
                
                # Validate point has required fields
                if "latitude" not in point or "longitude" not in point or "sequence_no" not in point:
                    db.session.rollback()
                    return {"error": "Each point must have latitude, longitude, and sequence_no"}, 400
                
                point_query = text("""
                    INSERT INTO CW2.Trail_Point 
                    (trail_point_id, trail_id, latitude, longitude, sequence_no)
                    VALUES (:point_id, :trail_id, :latitude, :longitude, :sequence_no)
                """)
                
                db.session.execute(point_query, {
                    "point_id": point_id,
                    "trail_id": trail_id,
                    "latitude": float(point["latitude"]),
                    "longitude": float(point["longitude"]),
                    "sequence_no": int(point["sequence_no"])
                })
                
                next_point_num += 1

        db.session.commit()

        # Fetch the created trail with points to return
        created_trail = Trail.query.get(trail_id)
        trail_data = trail_schema.dump(created_trail)
        
        # Add points to response
        points = Trail_Point.query.filter_by(trail_id=trail_id)\
                                  .order_by(Trail_Point.sequence_no).all()
        trail_data["points"] = trail_points_schema.dump(points)
        
        return trail_data, 201

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()
        
        # Check for specific constraint violations
        if "unique" in error_msg or "duplicate" in error_msg:
            if "trail_name" in error_msg or "uq_trail_name" in error_msg:
                return {"error": "Trail with this name already exists"}, 409
            elif "sequence_no" in error_msg:
                return {"error": "Duplicate sequence number in trail points"}, 400
        
        return {"error": "Data integrity violation", "details": str(e.orig)}, 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error occurred", "details": str(e)}, 500

    except Exception as e:
        db.session.rollback()
        return {"error": "Unexpected error", "details": str(e)}, 500


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
        trail_data = trail_schema.dump(updated_trail)
        
        # Add points to response
        points = Trail_Point.query.filter_by(trail_id=trail_id)\
                                  .order_by(Trail_Point.sequence_no).all()
        trail_data["points"] = trail_points_schema.dump(points)
        
        return trail_data, 200

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig).lower()
        
        if "unique" in error_msg or "duplicate" in error_msg:
            return {"error": "Trail with this name already exists"}, 409
            
        return {"error": "Data integrity violation", "details": str(e.orig)}, 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error occurred", "details": str(e)}, 500


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
        return {"error": "Database error occurred", "details": str(e)}, 500