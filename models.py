import pytz
from datetime import datetime
from marshmallow import Schema, fields
from config import db

class Users(db.Model):
    __tablename__ = "Users"  # FIXED: Double underscores!
    __table_args__ = {'schema': 'CW2'}  # FIXED: Double underscores!
    
    user_id = db.Column(db.String(7), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
    trails = db.relationship("Trails", backref="creator", lazy=True)

class Features(db.Model):
    __tablename__ = "Feature"  # FIXED: Double underscores!
    __table_args__ = {'schema': 'CW2'}  # FIXED: Double underscores!
    
    feature_id = db.Column(db.String(7), primary_key=True)
    feature_name = db.Column(db.String(100), nullable=False)
    
    trail_features = db.relationship("TrailFeatures", backref="feature", lazy=True)

class Trails(db.Model):
    __tablename__ = "Trail" 
    __table_args__ = {'schema': 'CW2'}
    
    trail_id = db.Column(db.String(7), primary_key=True)
    trail_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)  
    visibility = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    location_id = db.Column(db.String(7), db.ForeignKey("CW2.Location.location_id"))
    length = db.Column(db.Numeric(5, 2))
    estimated_time = db.Column(db.Numeric(4, 2))
    elevation_gain = db.Column(db.Integer)
    route_id = db.Column(db.String(7), db.ForeignKey("CW2.Route.route_id"), nullable=False)
    difficulty_id = db.Column(db.String(7), db.ForeignKey("CW2.Difficulty.difficulty_id"), nullable=False)
    created_by = db.Column(db.String(7), db.ForeignKey("CW2.Users.user_id"))
    
    trail_features = db.relationship("TrailFeatures", backref="trail", lazy=True)

class TrailFeatures(db.Model):
    __tablename__ = "Trail_Feature"  
    __table_args__ = {'schema': 'CW2'} 
    
    trail_feature_id = db.Column(db.String(8), primary_key=True)  
    trail_id = db.Column(db.String(7), db.ForeignKey("CW2.Trail.trail_id"))
    feature_id = db.Column(db.String(7), db.ForeignKey("CW2.Feature.feature_id"))

class UserSchema(Schema):
    user_id = fields.Str()
    username = fields.Str()
    email = fields.Str()
    role = fields.Str()

class FeatureSchema(Schema):
    feature_id = fields.Str()
    feature_name = fields.Str()

class TrailSchema(Schema):
    trail_id = fields.Str()
    trail_name = fields.Str()
    description = fields.Str()
    visibility = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    location_id = fields.Str()
    length = fields.Decimal()
    estimated_time = fields.Decimal()
    elevation_gain = fields.Int()
    route_id = fields.Str()
    difficulty_id = fields.Str()
    created_by = fields.Str()

class TrailFeatureSchema(Schema):
    trail_feature_id = fields.Str()
    trail_id = fields.Str()
    feature_id = fields.Str()

user_schema = UserSchema()
users_schema = UserSchema(many=True)
feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
trail_feature_schema = TrailFeatureSchema()
trail_features_schema = TrailFeatureSchema(many=True)