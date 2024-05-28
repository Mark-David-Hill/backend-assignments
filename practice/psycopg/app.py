import os

from flask import Flask, jsonify, request
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

app = Flask(__name__)


def create_tables():
    print("Creating tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR NOT NULL UNIQUE,
        description VARCHAR,
        price FLOAT,
        active BOOLEAN DEFAULT true
        );
    """)
    conn.commit()


@app.route('/product', methods=['POST'])
def product_create():
    post_data = request.form if request.form else request.json
    product_name = post_data.get("product_name")
    description = post_data.get("description")
    price = post_data.get("price")

    cursor.execute(
        """
        INSERT INTO Products
        (product_name, description, price)
        VALUES(%s, %s, %s)
        """,
        (product_name, description, price)
    )
    conn.commit()
    return jsonify({"message": f"{product_name} has been added to the Products table"}), 201


@app.route('/product/<product_id>', methods=['GET'])
def product_get_by_id(product_id):
    cursor.execute(
        """
        SELECT * FROM Products
        WHERE product_id=%s;
        """, [product_id]
    )
    result = cursor.fetchone()
    if result:
        return jsonify(({"message": "product found", "result": result})), 200
    else:
        return jsonify(({"message": f"No product found with product_id {product_id}"})), 404


@app.route('/products/<active_status>', methods=['GET'])
def products_get_by_activity(active_status):
    cursor.execute(
        """
        SELECT * FROM Products
        WHERE active=%s;
        """, [active_status]
    )
    results = cursor.fetchall()

    if results:
        product_list = []
        for product in results:
            product_record = {
                'product_id': product[0],
                'product_name': product[1],
                'description': product[2],
                'price': product[3],
                'active': product[4]
            }
            product_list.append(product_record)

        return jsonify(({"message": "product(s) found", "result": product_list})), 200
    else:
        return jsonify(({"message": f"No product found with the active status set to {active_status}"})), 404


@app.route('/product/<product_id>/<active_status>', methods=['PATCH'])
def product_update_activity(product_id, active_status):
    cursor.execute(
        """
        UPDATE Products
        SET active=%s
        WHERE product_id=%s;
        """, [active_status, product_id]
    )
    conn.commit()
    return jsonify({"message": f"product with product_id {product_id} set to {active_status}"}), 200


if __name__ == '__main__':
    create_tables()
    app.run(host=app_host, port=app_port)


# product_create('Monopoly', 'The game of negotiation and trade.', 14.95)
# product_create('Clue', 'The game of deception.', 9.95)
# product_get_by_id(3)
# products_get_by_activity(True)
# product_update_activity(2, False)
