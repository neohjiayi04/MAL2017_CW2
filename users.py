from flask import request, jsonify
from models import db, Users, users_schema
from marshmallow import Schema, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Single user schema
class UserSchema(Schema):
    user_id = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)

user_schema = UserSchema()

def get_users():
    items = Users.query.all()
    return jsonify(users_schema.dump(items)), 200

def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_schema.dump(user)), 200

def create_user(body):
    try:
        # Get the highest user_id and generate next one
        last_user = db.session.query(Users).order_by(Users.user_id.desc()).first()
        
        if last_user:
            last_num = int(last_user.user_id[1:])
            new_num = last_num + 1
        else:
            new_num = 1
        
        new_id = f"U{new_num:06d}"
        
        u = Users(
            user_id=new_id,
            username=body["username"],
            email=body["email"],
            password=body["password"],
            role=body.get("role", "user")
        )
        db.session.add(u)
        db.session.commit()
        return jsonify(user_schema.dump(u)), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Integrity error", "details": str(e.orig)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

def update_user(user_id, body):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        for key, value in body.items():
            if hasattr(user, key) and key != 'user_id':
                setattr(user, key, value)
        
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500