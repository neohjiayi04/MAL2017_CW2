from datetime import datetime
from config import app, db
from models import Users, Features, Trails, TrailFeatures

with app.app_context():
    db.drop_all()
    db.create_all()

    u1 = Users(
        user_id="U000001", 
        username="Jessica Lim", 
        email="jessica@gmail.com", 
        password="hashedPass123", 
        role="admin"
    )
    u2 = Users(
        user_id="U000002", 
        username="Grace Hopper", 
        email="grace@plymouth.ac.uk", 
        password="ISAD123!", 
        role="user"
    )

    f1 = Features(feature_id="F000001", feature_name="Beaches")
    f2 = Features(feature_id="F000002", feature_name="Pub walks")

    t1 = Trails(
        trail_id="T000001",
        trail_name="Bovisand to Jennycliff",
        description="Coastal walk in South Devon AONB",
        visibility="full",
        created_at=datetime(2025, 11, 18, 11, 1, 0),
        updated_at=datetime(2025, 11, 18, 11, 1, 0),
        location_id="L000002",
        length=5.80,
        estimated_time=2.00,
        elevation_gain=161,
        route_id="R000002",
        difficulty_id="D000002",
        created_by="U000001"
    )

    tf1 = TrailFeatures(trail_feature_id="TF000001", trail_id="T000001", feature_id="F000001")

    db.session.add_all([u1, u2, f1, f2, t1, tf1])
    db.session.commit()
    
    print("✓ Database built successfully!")