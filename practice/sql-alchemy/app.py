from flask import Flask, jsonify, request
import psycopg2
import os

from db import *

from models.products_categories_xref import products_categories_xref
from models.warranties import Warranties
from models.categories import Categories
from models.companies import Companies
from models.products import Products

import routes.warranties_routes
import routes.categories_routes
import routes.companies_routes
import routes.products_routes

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_PORT")
database_uri = os.environ.get("DATABASE_URI")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(routes.warranties_routes.warranties)
app.register_blueprint(routes.categories_routes.categories)
app.register_blueprint(routes.companies_routes.companies)
app.register_blueprint(routes.products_routes.products)

init_db(app, db)


def create_tables():
    with app.app_context():
        print("creating tables...")
        db.create_all()
        print("tables created successfully")


create_tables()


if __name__ == "__main__":
    app.run(host=flask_host, port=flask_port)
