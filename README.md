# TrailService Microservice API

**Student ID:** BSSE2506008

**Module:** MAL2017 Information Management & Retrieval  

**Assessment:** Coursework 2 -  Report on Micro-service Implementation


## Project Description
This microservice provides RESTful API endpoints for managing hiking trails as part of a larger wellbeing trail application. It implements full CRUD operations for trails, integrates with an external COMP2001 Authenticator API, and stores all data in a normalized Microsoft SQL Server database.


## 📌 Features

✅ Full CRUD operations on trails

✅ Authentication integration with external API

✅ Reference data endpoints (locations, routes, difficulties, features)

✅ Trail visibility control (full/limited)

✅ Automated audit logging via SQL triggers

✅ RESTful API with OpenAPI 3.0 and Swagger UI documentation

✅ Comprehensive error handling with appropriate HTTP status codes


## 🧰 Technology Stack
- **Backend:** Python 3.x, Flask, Connexion
- **Database:** Microsoft SQL Server
- **ORM:** SQLAlchemy
- **Validation:** Marshmallow
- **Documentation:** OpenAPI/Swagger UI


## 🗄️ Database Schema
The database uses schema `CW2` with the following tables:
- Users
- Location
- Route
- Trail_Point
- Difficulty
- Feature
- Trail
- Trail_Feature (junction table)
- Trail_Log (audit table)


## 🚀 Installation & Setup

1. Clone the repository:
git clone https://github.com/neohjiayi04/MAL2017_CW2.git
cd MAL2017_CW2

2.  Install dependencies:
pip install -r requirements.txt

3. Configure database connection:
Update config.py with your database credentials

4. Set up database:
run `python setup_database.py`

5. Start the application:
python app.py

6. Access Swagger UI:
[http://localhost:5000/ui
](http://127.0.0.1:5000/ui/)


## 🔗 API Endpoints

### Authentication
- POST /login - Authenticate user via external COMP2001 API
  
### Trails
- `GET /trails` - List all trails
- `GET /trails/{id}` - Get specific trail
- `POST /trails` - Create trail (requires auth)
- `PUT /trails/{id}` - Update trail (requires auth + ownership)
- `DELETE /trails/{id}` - Delete trail (requires auth + ownership)
  
### Reference Data (Read-Only)
- GET /reference/locations - Available trail locations
- GET /reference/routes - Route types
- GET /reference/difficulties - Difficulty levels
- GET /reference/features - Trail features


## 🛠️Testing
Use Swagger UI at `http://localhost:5000/ui` to test all endpoints interactively.


## ✒️ Report
Full documentation available in the assessment report PDF.


## 📄 License
This project is created for educational purposes as part of university coursework.
