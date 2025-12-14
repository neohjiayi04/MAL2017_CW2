# TrailService Microservice API

**Student ID:** BSSE2506008

**Module:** MAL2017 Information Management & Retrieval  

**Assessment:** Coursework 2 -  Report on Micro-service Implementation


## Project Description
This microservice provides RESTful API endpoints for managing hiking trails as part of a larger wellbeing trail application. It implements full CRUD operations with authentication integration.


## 📌 Features

✅ Full CRUD operations on trails, users, features

✅ Authentication integration with external API

✅ Role-based visibility (full/limited)

✅ Many-to-many relationship (trails-features)

✅ Audit trail logging

✅ RESTful API with Swagger documentation


## 🧰 Technology Stack
- **Backend:** Python 3.x, Flask, Connexion
- **Database:** Microsoft SQL Server
- **ORM:** SQLAlchemy
- **Validation:** Marshmallow
- **Documentation:** OpenAPI/Swagger


## 🗄️ Database Schema
The database uses schema `CW2` with the following tables:
- Users
- Location
- Route
- Difficulty
- Feature
- Trail
- Trail_Feature (junction table)
- Trail_Log (audit table)


## 🚀 Installation & Setup

1. Install dependencies:
pip install -r requirements.txt

2. Set up database:
run `python setup_database.py`

3. Start the application:
python app.py

4. Access Swagger UI:
[http://localhost:5000/ui
](http://127.0.0.1:5000/ui/)


## 🔗 API Endpoints

### Trails
- `GET /trails` - List all trails
- `GET /trails/{id}` - Get specific trail
- `POST /trails` - Create trail (requires auth)
- `PUT /trails/{id}` - Update trail (requires auth + ownership)
- `DELETE /trails/{id}` - Delete trail (requires auth + ownership)
  
Similar endpoints for Users, Features, Trail_Features


## 🛠️Testing
Use Swagger UI at `http://localhost:5000/ui` to test all endpoints interactively.


## ✒️ Report
Full documentation available in the assessment report PDF.


## 📄 License
This project is created for educational purposes as part of university coursework.
