import pyodbc

# Connection string
conn_str = (
    "Driver={SQL Server};"
    "Server=localhost;"
    "Database=CW2;"
    "UID=SA;"
    "PWD=C0mp2001!;"
    "TrustServerCertificate=yes;"
)

# SQL Script
sql_script = """
-- Use your database
USE CW2;
GO

-- Drop existing objects (in correct order - dependent objects first)
IF OBJECT_ID('CW2.vw_TrailDetails', 'V') IS NOT NULL DROP VIEW CW2.vw_TrailDetails;
IF OBJECT_ID('CW2.trgTrailInsert', 'TR') IS NOT NULL DROP TRIGGER CW2.trgTrailInsert;
IF OBJECT_ID('CW2.Trail_Point', 'U') IS NOT NULL DROP TABLE CW2.Trail_Point;
IF OBJECT_ID('CW2.Trail_Feature', 'U') IS NOT NULL DROP TABLE CW2.Trail_Feature;
IF OBJECT_ID('CW2.Trail_Log', 'U') IS NOT NULL DROP TABLE CW2.Trail_Log;
IF OBJECT_ID('CW2.Trail', 'U') IS NOT NULL DROP TABLE CW2.Trail;
IF OBJECT_ID('CW2.Feature', 'U') IS NOT NULL DROP TABLE CW2.Feature;
IF OBJECT_ID('CW2.Location', 'U') IS NOT NULL DROP TABLE CW2.Location;
IF OBJECT_ID('CW2.Difficulty', 'U') IS NOT NULL DROP TABLE CW2.Difficulty;
IF OBJECT_ID('CW2.Route', 'U') IS NOT NULL DROP TABLE CW2.Route;
IF OBJECT_ID('CW2.Users', 'U') IS NOT NULL DROP TABLE CW2.Users;
GO

-- Create schema if not exists
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'CW2')
BEGIN
    EXEC('CREATE SCHEMA CW2');
END
GO

-- User Table
CREATE TABLE CW2.Users (
    user_id VARCHAR(7) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
   
    CONSTRAINT CK_User_ID_Format
        CHECK (user_id LIKE 'U[0-9][0-9][0-9][0-9][0-9][0-9]'),
   
    CONSTRAINT CK_User_Email_Format
        CHECK (email LIKE '_%@_%._%'),
   
    CONSTRAINT CK_User_Password_Format
        CHECK (LEN(password) >= 8 AND
               password LIKE '%[A-Za-z]%' AND password LIKE '%[0-9]%'),
   
    CONSTRAINT CK_User_Role
        CHECK (role IN ('admin','user'))
);
GO

-- Route Table
CREATE TABLE CW2.Route (
    route_id VARCHAR(7) PRIMARY KEY,
    route_type VARCHAR(50) NOT NULL,
   
    CONSTRAINT CK_Route_ID_Format
        CHECK (route_id LIKE 'R[0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_Route_Type
        CHECK (route_type IN ('loop', 'out-and-back', 'point-to-point'))
);
GO

-- Difficulty Table
CREATE TABLE CW2.Difficulty (
    difficulty_id VARCHAR(7) PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
   
    CONSTRAINT CK_Difficulty_ID_Format
        CHECK (difficulty_id LIKE 'D[0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_Difficulty_Level
        CHECK (level IN ('easy','moderate','hard','strenuous'))
);
GO

-- Location Table
CREATE TABLE CW2.Location (
    location_id VARCHAR(7) PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
   
    CONSTRAINT CK_Location_ID_Format
        CHECK (location_id LIKE 'L[0-9][0-9][0-9][0-9][0-9][0-9]')
);
GO

-- Feature Table
CREATE TABLE CW2.Feature (
    feature_id VARCHAR(7) PRIMARY KEY,
    feature_name VARCHAR(50) NOT NULL,
   
    CONSTRAINT CK_Feature_ID_Format
        CHECK (feature_id LIKE 'F[0-9][0-9][0-9][0-9][0-9][0-9]'),
   
    CONSTRAINT CK_Feature_Name
        CHECK (feature_name IN (
            'Beaches', 'Caves', 'City walks', 'Events', 'Forests',
            'Historic sites', 'Hot springs', 'Lakes', 'Pub walks',
            'Rail trails', 'Rivers', 'Views', 'Waterfalls',
            'Wildflowers', 'Wildlife'
        ))
);
GO

-- Trail Table
CREATE TABLE CW2.Trail (
    trail_id VARCHAR(7) PRIMARY KEY,
    trail_name VARCHAR(100) NOT NULL,
    description NVARCHAR(MAX) NULL,
    visibility VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    location_id VARCHAR(7) NULL,
    length DECIMAL(5,2) NULL,
    estimated_time DECIMAL(4,2) NULL,
    elevation_gain INT NULL,
    route_id VARCHAR(7) NOT NULL,
    difficulty_id VARCHAR(7) NOT NULL,
    created_by VARCHAR(7),
   
    CONSTRAINT CK_Trail_ID_Format
        CHECK (trail_id LIKE 'T[0-9][0-9][0-9][0-9][0-9][0-9]'),
   
    CONSTRAINT CK_Trail_Visibility
        CHECK (visibility IN ('full','limited')),
   
    CONSTRAINT CK_Trail_Length
        CHECK (length IS NULL OR (length >= 0.01 AND length <= 999.99)),
   
    CONSTRAINT CK_Trail_EstimatedTime
        CHECK (estimated_time IS NULL OR (estimated_time >= 0.01 AND estimated_time <= 99.99)),
   
    CONSTRAINT CK_Trail_ElevationGain
        CHECK (elevation_gain IS NULL OR elevation_gain > 0),
   
    CONSTRAINT FK_Trail_Location
        FOREIGN KEY (location_id) REFERENCES CW2.Location(location_id),
   
    CONSTRAINT FK_Trail_Route
        FOREIGN KEY (route_id) REFERENCES CW2.Route(route_id),
   
    CONSTRAINT FK_Trail_CreatedBy
        FOREIGN KEY (created_by) REFERENCES CW2.Users(user_id),
   
    CONSTRAINT FK_Trail_Difficulty
        FOREIGN KEY (difficulty_id) REFERENCES CW2.Difficulty(difficulty_id)
);
GO

-- Trail Point Table
CREATE TABLE CW2.Trail_Point (
    trail_point_id VARCHAR(8) PRIMARY KEY,
    trail_id VARCHAR(7) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    sequence_no INT NOT NULL,

    CONSTRAINT CK_TrailPoint_ID_Format
        CHECK (trail_point_id LIKE 'TP[0-9][0-9][0-9][0-9][0-9][0-9]'),

    CONSTRAINT FK_TrailPoint_Trail
        FOREIGN KEY (trail_id)
        REFERENCES CW2.Trail(trail_id)
        ON DELETE CASCADE,

    CONSTRAINT UQ_TrailPoint_Order
        UNIQUE (trail_id, sequence_no)
);
GO

-- Trail Feature Table
CREATE TABLE CW2.Trail_Feature (
    trail_feature_id VARCHAR(8) PRIMARY KEY,
    feature_id VARCHAR(7) NOT NULL,
    trail_id VARCHAR(7) NOT NULL,
   
    CONSTRAINT CK_TrailFeature_ID_Format
        CHECK (trail_feature_id LIKE 'TF[0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT FK_TrailFeature_Feature
        FOREIGN KEY (feature_id) REFERENCES CW2.Feature(feature_id),
    CONSTRAINT FK_TrailFeature_Trail
        FOREIGN KEY (trail_id) REFERENCES CW2.Trail(trail_id) ON DELETE CASCADE,
    CONSTRAINT UQ_TrailFeature UNIQUE (trail_id, feature_id)
);
GO

-- Trail Log Table
CREATE TABLE CW2.Trail_Log (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    trail_id VARCHAR(7) NOT NULL,
    trail_name VARCHAR(100) NOT NULL,
    added_by VARCHAR(7) NOT NULL,
    added_on DATETIME NOT NULL DEFAULT GETDATE()
);
GO


INSERT INTO CW2.Users (user_id, username, email, password, role) VALUES
('U000001', 'Jessica Lim', 'jessica@gmail.com', 'hashedPass123', 'admin'),
('U000002', 'Grace Hopper', 'grace@plymouth.ac.uk', 'ISAD123!', 'user'),
('U000003', 'Ada Lovelace', 'ada@plymouth.ac.uk', 'AhaPass2!', 'user'),
('U000004', 'Tim Berners-Lee', 'tim@plymouth.ac.uk', 'COMP2001!', 'user');
GO

INSERT INTO CW2.Route (route_id, route_type) VALUES
('R000001', 'loop'),
('R000002', 'out-and-back'),
('R000003', 'point-to-point');
GO

INSERT INTO CW2.Difficulty (difficulty_id, level) VALUES
('D000001', 'easy'),
('D000002', 'moderate'),
('D000003', 'hard'),
('D000004', 'strenuous');
GO

INSERT INTO CW2.Location (location_id, location_name, region, country) VALUES
('L000001', 'Plymouth', 'Devon', 'England'),
('L000002', 'South Devon National Landscape (AONB)', 'Devon', 'England'),
('L000003', 'Lake District National Park', 'Cumbria', 'England'),
('L000004', 'Rocky Mountain National Park', 'Colorado', 'United States'),
('L000005', 'Kuala Lumpur', 'Kuala Lumpur', 'Malaysia'),
('L000006', 'Subang Jaya', 'Selangor', 'Malaysia');
GO

INSERT INTO CW2.Feature (feature_id, feature_name) VALUES
('F000001', 'Beaches'),
('F000002', 'Caves'),
('F000003', 'City walks'),
('F000004', 'Events'),
('F000005', 'Forests'),
('F000006', 'Historic sites'),
('F000007', 'Hot springs'),
('F000008', 'Lakes'),
('F000009', 'Pub walks'),
('F000010', 'Rail trails'),
('F000011', 'Rivers'),
('F000012', 'Views'),
('F000013', 'Waterfalls'),
('F000014', 'Wildflowers'),
('F000015', 'Wildlife');
GO

INSERT INTO CW2.Trail (
    trail_id, trail_name, description, visibility, created_at, updated_at,
    location_id, length, estimated_time, elevation_gain, route_id, difficulty_id, created_by
) VALUES
('T000001', 'Bovisand to Jennycliff',
    'Coastal walk in South Devon AONB along the coastal path going north then back. Begin from the car park just south of Bovisand Beach. By the golf course, you can turn back or continue north. Keep an eye out for flying golf balls. Lovely route for any rambler, any time of the year.',
    'full', '2025-11-18 11:01:00', '2025-11-18 11:01:00',
    'L000002', 5.80, 2.00, 161, 'R000002', 'D000002', 'U000001'),
('T000002', 'Sri Bintang Hill',
    'Bukit Sri Bintang (Bukit Pelangi) is a popular hiking destination in Kuala Lumpur, Malaysia. Features scenic views and moderate difficulty.',
    'full', '2025-11-18 11:02:00', '2025-11-18 11:02:00',
    'L000005', 2.30, 1.50, 198, 'R000001', 'D000002', 'U000001'),
('T000003', 'Plymbridge Circular',
    'Gentle circular walk through ancient oak woodlands beside the River Plym. Includes industrial remains and breathtaking views from the viaduct. Wildlife such as kingfishers, sea trout, dippers, peregrine falcon, and deer may be seen. First half is quiet and hidden, ideal for dogs. Second half follows the river and railway line back south to complete the loop.',
    'full', '2025-11-18 11:03:00', '2025-11-18 11:03:00',
    'L000001', 5.00, 2.00, 147, 'R000001', 'D000001', 'U000001'),
('T000004', 'Kingsley Hill Peak Loop',
    'The loop trail consists of a dirt trail with several steep and challenging climbs, making it a great location for a daily workout. Upon reaching the summit, hikers will be treated to expansive panoramic views, encompassing the urban landscape of Putra Heights, Subang Jaya, and the surrounding areas. The hill is a prime example of a natural space in the heart of the city that is valued and maintained by the community for the mutual benefit.',
    'full', '2025-11-18 11:03:00', '2025-11-25 18:03:00',
    'L000006', 3.4, 1.50, 185, 'R000001', 'D000002', 'U000001');
GO

INSERT INTO CW2.Trail_Point (trail_point_id, trail_id, sequence_no, latitude, longitude) VALUES
-- Points for T000001 (Bovisand to Jennycliff)
('TP000001', 'T000001', 1, 50.351234, -4.135678),
('TP000002', 'T000001', 2, 50.352010, -4.138900),
('TP000003', 'T000001', 3, 50.353456, -4.142300),

-- Points for T000002 (Sri Bintang Hill)
('TP000004', 'T000002', 1, 3.156789, 101.672345),
('TP000005', 'T000002', 2, 3.157890, 101.673456),
('TP000006', 'T000002', 3, 3.158901, 101.674567),

-- Points for T000003 (Plymbridge Circular)
('TP000007', 'T000003', 1, 50.412345, -4.098765),
('TP000008', 'T000003', 2, 50.413456, -4.097654),
('TP000009', 'T000003', 3, 50.414567, -4.096543),

-- Points for T000004 (Kingsley Hill Peak Loop)
('TP000010', 'T000004', 1, 3.048123, 101.585234),
('TP000011', 'T000004', 2, 3.049234, 101.586345),
('TP000012', 'T000004', 3, 3.050345, 101.587456);
GO

INSERT INTO CW2.Trail_Feature (trail_feature_id, feature_id, trail_id) VALUES
    ('TF000001', 'F000001', 'T000001'),
    ('TF000002', 'F000009', 'T000001'),
    ('TF000003', 'F000012', 'T000002'),
    ('TF000004', 'F000014', 'T000003'),
    ('TF000005', 'F000015', 'T000003'),
    ('TF000006', 'F000011', 'T000003'),
    ('TF000007', 'F000008', 'T000004'),
    ('TF000008', 'F000012', 'T000004'),
    ('TF000009', 'F000005', 'T000004'),
    ('TF000010', 'F000013', 'T000004'),
    ('TF000011', 'F000014', 'T000004');
GO

-- Create Trigger
CREATE TRIGGER CW2.trgTrailInsert
ON CW2.Trail
AFTER INSERT
AS
BEGIN
    INSERT INTO CW2.Trail_Log (trail_id, trail_name, added_by, added_on)
    SELECT i.trail_id, i.trail_name, i.created_by, GETDATE()
    FROM inserted i;
END;
GO

-- Create View
CREATE VIEW CW2.vw_TrailDetails AS 
SELECT  
    t.trail_id, 
    t.trail_name, 
    t.description, 
    t.visibility, 
    t.length, 
    t.estimated_time, 
    t.elevation_gain, 
    t.created_at, 
    t.updated_at, 
    l.location_name, 
    l.region, 
    l.country, 
    r.route_type, 
    d.level as difficulty_level, 
    u.username as created_by_name, 
    u.email as creator_email,
    t.created_by,
    STRING_AGG(f.feature_name, ', ') WITHIN GROUP (ORDER BY f.feature_name) as features 
FROM CW2.Trail t 
LEFT JOIN CW2.Location l ON t.location_id = l.location_id 
LEFT JOIN CW2.Route r ON t.route_id = r.route_id 
LEFT JOIN CW2.Difficulty d ON t.difficulty_id = d.difficulty_id 
LEFT JOIN CW2.Users u ON t.created_by = u.user_id 
LEFT JOIN CW2.Trail_Feature tf ON t.trail_id = tf.trail_id 
LEFT JOIN CW2.Feature f ON tf.feature_id = f.feature_id 
GROUP BY  
    t.trail_id, t.trail_name, t.description, t.visibility, 
    t.length, t.estimated_time, t.elevation_gain, 
    t.created_at, t.updated_at, l.location_name, l.region, 
    l.country, r.route_type, d.level, u.username, u.email, t.created_by;
GO

PRINT 'Database setup completed successfully!';
"""

try:
    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Split by GO statements and execute each batch
    batches = sql_script.split('GO')
    
    for i, batch in enumerate(batches, 1):
        if batch.strip():
            try:
                cursor.execute(batch)
                conn.commit()
                print(f"✓ Batch {i} executed successfully")
            except Exception as e:
                print(f"✗ Error in batch {i}: {e}")
                continue
    
    print("\n✅ Database setup completed successfully!")

    # Verify tables
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'CW2'
        ORDER BY TABLE_NAME
    """)
    
    print("\n📋 Tables created:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}")
    
    # Verify data counts
    print("\n📊 Data verification:")
    cursor.execute("SELECT COUNT(*) FROM CW2.Users")
    print(f"  Users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM CW2.Feature")
    print(f"  Features: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM CW2.Trail")
    print(f"  Trails: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM CW2.Trail_Point")
    print(f"  Trail Points: {cursor.fetchone()[0]}")  # ✅ Added this check
    
    # Show points per trail
    print("\n📍 Trail Points Distribution:")
    cursor.execute("""
        SELECT 
            t.trail_id,
            t.trail_name,
            COUNT(tp.trail_point_id) as point_count
        FROM CW2.Trail t
        LEFT JOIN CW2.Trail_Point tp ON t.trail_id = tp.trail_id
        GROUP BY t.trail_id, t.trail_name
        ORDER BY t.trail_id
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]} ({row[1]}): {row[2]} points")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")