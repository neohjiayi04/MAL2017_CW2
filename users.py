from flask import request, jsonify
from models import db, Users, users_schema
from marshmallow import Schema, fields
from sqlalchemy.exc import SQLAlchemyError

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
        u = Users(
            user_id=body["user_id"],
            username=body["username"],
            email=body["email"],
            password=body["password"],
            role=body.get("role", "user")
        )
        db.session.add(u)
        db.session.commit()
        return jsonify(user_schema.dump(u)), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

def update_user(user_id, body):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        for key, value in body.items():
            if hasattr(user, key):
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