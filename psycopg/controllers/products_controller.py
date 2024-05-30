import os

from flask import jsonify
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def product_create(request):
    post_data = request.form if request.form else request.json
    company_id = post_data['company_id']
    product_name = post_data['product_name']
    price = post_data['price']
    description = post_data['description']

    if not product_name:
        return jsonify({"message": "product_name is a Required Field"}), 400

    cursor.execute("""
        SELECT * FROM Products
        WHERE product_name=%s""",
                   [product_name])
    result = cursor.fetchone()
    if result:
        return jsonify({"message": 'Product already exists'}), 400

    try:
        cursor.execute(
            """
            INSERT INTO Products
            (company_id, product_name, price, description)
            VALUES(%s, %s, %s, %s);
            """,
            [company_id, product_name, price, description]
        )
        conn.commit()

    except:
        return jsonify({"message": "Product could not be added"}), 404

    return jsonify({"message": f"{product_name} has been added to the Products table."}), 200


def products_get():
    try:
        cursor.execute(
            """
            SELECT c.category_id, c.category_name, w.warranty_id, w.warranty_months, p.product_name, p.price, p.description
            FROM Products p
            INNER JOIN ProductsCategoriesXref x ON (p.product_id = x.product_id)
            INNER JOIN Categories c ON (x.category_id = c.category_id)
            INNER JOIN Warranties w ON (p.product_id = w.product_id)
            """
        )
        result = cursor.fetchall()
        if result:
            return jsonify(({"message": "products found", "result": result})), 200
        else:
            return jsonify(({"message": f"No products found"})), 404
    except:
        return jsonify({"message": "Could not fetch products data"}), 404


def products_get_active():
    try:
        cursor.execute(
            """
            SELECT *    
            FROM Products
            WHERE active=%s
            """, [True]
        )
        result = cursor.fetchall()
        if result:
            return jsonify(({"message": "active products found", "result": result})), 200
        else:
            return jsonify(({"message": f"No active products found"})), 404
    except:
        return jsonify({"message": "Could not fetch products data"}), 404


def product_get_by_id(product_id):
    try:
        cursor.execute(
            """
            SELECT c.category_id, c.category_name, p.product_name, p.price, p.description
            FROM Products p
            INNER JOIN ProductsCategoriesXref x ON (p.product_id = x.product_id)
            INNER JOIN Categories c ON (x.category_id = c.category_id)
            WHERE p.product_id=%s;
            """, [product_id]
        )
        result = cursor.fetchall()
        if result:
            return jsonify(({"message": f"product with id {product_id} found", "result": result})), 200
        else:
            return jsonify(({"message": "No product found"})), 404
    except:
        return jsonify({"message": "Could not fetch product data"}), 404


def product_update_by_id(request, product_id):
    data = request.form if request.form else request.json
    product = {}
    product['product_id'] = int(product_id)

    if not product['product_id']:
        return jsonify({"message": 'product_id is required'}), 400

    for record in product_records:
        if record['product_id'] == product['product_id']:
            product = record

    product['product_name'] = data.get('product_name', product['product_name'])
    product['description'] = data.get('description', product['description'])
    product['price'] = data.get('price', product['price'])
    product['active'] = data.get('active', product['active'])

    return jsonify({"message": f"product {product['product_name']} has been updated", "results": product}), 200


def product_update_active_status(product_id):
    product = {}
    product['product_id'] = int(product_id)

    if not product['product_id']:
        return jsonify({"message": 'product_id is required'}), 400

    for record in product_records:
        if record['product_id'] == product['product_id']:
            product = record

    product['active'] = not product['active']

    return jsonify({"message": f"product {product['product_name']}'s active status has been set to {product['active']}", "results": product}), 200


def product_delete(product_id):
    product = {}
    product['product_id'] = int(product_id)

    if not product['product_id']:
        return jsonify({"message": 'product_id is required'}), 400

    for record in product_records:
        if record['product_id'] == product['product_id']:
            product = record

    product_records.remove(product)

    return jsonify({"message": f"product {product['product_name']} has been deleted."}), 200
