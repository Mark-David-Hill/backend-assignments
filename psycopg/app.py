import os

from flask import Flask
import psycopg2

import routes
from db import create_tables

database_name = os.environ.get('DATABASE_NAME')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

app = Flask(__name__)

app.register_blueprint(routes.product)
app.register_blueprint(routes.company)
app.register_blueprint(routes.warranty)
app.register_blueprint(routes.category)


if __name__ == '__main__':
    create_tables(conn, cursor)
    app.run(host='0.0.0.0', port='8086')
