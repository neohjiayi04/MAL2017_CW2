import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()

connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc://SA:C0mp2001!@localhost/CW2?"
    "driver=SQL+Server&"
    "TrustServerCertificate=yes&"
    "LongAsMax=yes"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "fast_executemany": True,
}

db = SQLAlchemy(app)
ma = Marshmallow(app)