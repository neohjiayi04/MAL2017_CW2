# app.py

from flask import render_template, redirect

import config
from models import Trails  

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route("/")
def home():
    # Redirect to the Swagger UI
    return redirect("/ui")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)