from flask import abort, make_response, request, jsonify
from config import db
from models import Users, users_schema

def read_all():
    users = Users.query.all()
    return users_schema.dump(users)

def read_one(user_id):
    user = Users.query.get(user_id)
    if not user:
        abort(404)
    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    })


def create():
    data = request.json
    new_user = Users(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201


def update(user_id):
    user = Users.query.get(user_id)
    if not user:
        abort(404)
    data = request.json
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify({"message": "User updated"})


def delete(user_id):
    user = Users.query.get(user_id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return "", 204
