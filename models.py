# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}

    user_id = db.Column(db.String(7), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Route(db.Model):
    __tablename__ = 'Route'
    __table_args__ = {'schema': 'CW2'}

    route_id = db.Column(db.String(7), primary_key=True)
    route_type = db.Column(db.String(50), nullable=False)

class Difficulty(db.Model):
    __tablename__ = 'Difficulty'
    __table_args__ = {'schema': 'CW2'}

    difficulty_id = db.Column(db.String(7), primary_key=True)
    level = db.Column(db.String(20), nullable=False)

class Location(db.Model):
    __tablename__ = 'Location'
    __table_args__ = {'schema': 'CW2'}

    location_id = db.Column(db.String(7), primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

class Feature(db.Model):
    __tablename__ = 'Feature'
    __table_args__ = {'schema': 'CW2'}

    feature_id = db.Column(db.String(7), primary_key=True)
    feature_name = db.Column(db.String(50), nullable=False)

class Trail(db.Model):
    __tablename__ = 'Trail'
    __table_args__ = {'schema': 'CW2'}

    trail_id = db.Column(db.String(7), primary_key=True)
    trail_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    visibility = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    location_id = db.Column(db.String(7), db.ForeignKey('CW2.Location.location_id'), nullable=True)
    length = db.Column(db.Numeric(5,2), nullable=True)
    estimated_time = db.Column(db.Numeric(4,2), nullable=True)
    elevation_gain = db.Column(db.Integer, nullable=True)
    route_id = db.Column(db.String(7), db.ForeignKey('CW2.Route.route_id'), nullable=False)
    difficulty_id = db.Column(db.String(7), db.ForeignKey('CW2.Difficulty.difficulty_id'), nullable=False)
    created_by = db.Column(db.String(7), db.ForeignKey('CW2.Users.user_id'), nullable=True)

class Trail_Feature(db.Model):
    __tablename__ = 'Trail_Feature'
    __table_args__ = {'schema': 'CW2'}

    trail_feature_id = db.Column(db.String(8), primary_key=True)
    feature_id = db.Column(db.String(7), db.ForeignKey('CW2.Feature.feature_id'), nullable=False)
    trail_id = db.Column(db.String(7), db.ForeignKey('CW2.Trail.trail_id'), nullable=False)

class Trail_Log(db.Model):
    __tablename__ = 'Trail_Log'
    __table_args__ = {'schema': 'CW2'}

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_id = db.Column(db.String(7), nullable=False)
    trail_name = db.Column(db.String(100), nullable=False)
    added_by = db.Column(db.String(7), nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# ---------- SCHEMAS ----------

class UsersSchema(Schema):
    user_id = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)

class FeatureSchema(Schema):
    feature_id = fields.Str(required=True)
    feature_name = fields.Str(required=True)

class TrailSchema(Schema):
    trail_id = fields.Str(required=True)
    trail_name = fields.Str(required=True)
    description = fields.Str()
    visibility = fields.Str(validate=validate.OneOf(["full","limited"]), required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    location_id = fields.Str()
    length = fields.Float()
    estimated_time = fields.Float()
    elevation_gain = fields.Int()
    route_id = fields.Str(required=True)
    difficulty_id = fields.Str(required=True)
    created_by = fields.Str(required=True)

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)
users_schema = UsersSchema(many=True)
