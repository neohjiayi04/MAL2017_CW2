🗺️ **TrailService Microservice API** 🏞️

**Module**: MAL2017 Information Management & Retrieval
Assessment 2: Report on Micro-service Implementation
**Student ID**: BSSE2506008
A microservice providing RESTful API endpoints for managing hiking trails within a wellbeing trail application. The service supports full CRUD operations, authentication, and audit logging, following REST and OpenAPI design principles.

📌 **Features**
✔️ Full CRUD operations for Trails, Users, Features, and Trail_Features
✔️ External authentication integration
✔️ Role-based visibility control (full / limited)
✔️ Many-to-many Trail ↔ Feature relationship
✔️ Automatic audit entries (Trail_Log) via SQL trigger
✔️ OpenAPI/Swagger documentation with interactive testing
✔️ SQLAlchemy ORM + Marshmallow validation

🧰 **Technology Stack**
**Backend**: Python 3.x, Flask, Connexion
**Database**:	Microsoft SQL Server
**ORM**:	SQLAlchemy
**Validation**:	Marshmallow
**Documentation**:	OpenAPI / Swagger UI

🗄️ **Database Schema Overview**
The microservice uses schema CW2 containing:
- Users
- Location
- Route
- Difficulty
- Feature
- Trail
- Trail_Feature (junction table)
- Trail_Log (audit table via trigger)
A logging trigger inserts entries into Trail_Log whenever a new trail is created.

🚀 **Installation & Setup**
1.**Install dependencies**: pip install -r requirements.txt
2. **Set up the database**: python build_database.py
3. **Start the application**: python app.py
4. **Access interactive API documentation**: http://127.0.0.1:5000

🔗 **API Endpoints Overview**
- `GET /trails` - List all trails
- `GET /trails/{id}` - Get specific trail
- `POST /trails` - Create trail (requires auth)
- `PUT /trails/{id}` - Update trail (requires auth + ownership)
- `DELETE /trails/{id}` - Delete trail (requires auth + ownership)
### Similar endpoints for Users, Features, Trail_Features

## Testing
Use Swagger UI to test all endpoints interactively.

## Report
Full documentation available in the assessment report PDF.

## License
This project is created for educational purposes as part of university coursework.
