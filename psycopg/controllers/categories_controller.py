import os

from flask import jsonify
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def category_create(request):
    post_data = request.form if request.form else request.json
    category_name = post_data['category_name']

    if not category_name:
        return jsonify({"message": "category_name is a Required Field"}), 400

    cursor.execute("""
        SELECT * FROM Categories
        WHERE category_name=%s""",
                   [category_name])
    result = cursor.fetchone()
    if result:
        return jsonify({"message": 'Category already exists'}), 400

    try:
        cursor.execute(
            """
            INSERT INTO Categories
            (category_name)
            VALUES(%s);
            """,
            [category_name]
        )
        conn.commit()

    except:
        return jsonify({"message": "Product could not be added"}), 404

    return jsonify({"message": f"{category_name} has been added to the Categories table."}), 200


def categories_get():
    try:
        cursor.execute(
            """
            SELECT *
            FROM Categories;
            """
        )
        result = cursor.fetchall()
        if result:
            return jsonify(({"message": "categories found", "result": result})), 200
        else:
            return jsonify(({"message": f"No categories found"})), 404
    except:
        return jsonify({"message": "Could not fetch categories data"}), 404


def category_get_by_id(category_id):
    try:
        cursor.execute(
            """
            SELECT *
            FROM Categories
            WHERE category_id=%s;
            """, [category_id]
        )
        result = cursor.fetchone()
        if result:
            return jsonify(({"message": f"category with id {category_id} found", "result": result})), 200
        else:
            return jsonify(({"message": "No category found"})), 404
    except:
        return jsonify({"message": "Could not fetch category data"}), 404


# def product_update_by_id(request, product_id):
#     data = request.form if request.form else request.json
#     product = {}
#     product['product_id'] = int(product_id)

#     if not product['product_id']:
#         return jsonify({"message": 'product_id is required'}), 400

#     for record in product_records:
#         if record['product_id'] == product['product_id']:
#             product = record

#     product['product_name'] = data.get('product_name', product['product_name'])
#     product['description'] = data.get('description', product['description'])
#     product['price'] = data.get('price', product['price'])
#     product['active'] = data.get('active', product['active'])

#     return jsonify({"message": f"product {product['product_name']} has been updated", "results": product}), 200


# def product_update_active_status(product_id):
#     product = {}
#     product['product_id'] = int(product_id)

#     if not product['product_id']:
#         return jsonify({"message": 'product_id is required'}), 400

#     for record in product_records:
#         if record['product_id'] == product['product_id']:
#             product = record

#     product['active'] = not product['active']

#     return jsonify({"message": f"product {product['product_name']}'s active status has been set to {product['active']}", "results": product}), 200


# def product_delete(product_id):
#     product = {}
#     product['product_id'] = int(product_id)

#     if not product['product_id']:
#         return jsonify({"message": 'product_id is required'}), 400

#     for record in product_records:
#         if record['product_id'] == product['product_id']:
#             product = record

#     product_records.remove(product)

#     return jsonify({"message": f"product {product['product_name']} has been deleted."}), 200
