from flask import Flask
import psycopg2
import os

from db import *
from util.blueprints import register_blueprints

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_PORT")
database_uri = os.environ.get("DATABASE_URI")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

register_blueprints(app)

init_db(app, db)


def create_tables():
    with app.app_context():
        print("creating tables...")
        db.create_all()
        print("tables created successfully")


create_tables()

if __name__ == "__main__":
    app.run(host=flask_host, port=flask_port)
