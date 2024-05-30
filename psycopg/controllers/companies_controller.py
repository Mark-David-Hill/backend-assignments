import os

from flask import jsonify
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def company_create(request):
    post_data = request.form if request.form else request.json
    company_name = post_data['company_name']

    if not company_name:
        return jsonify({"message": "company_name is a Required Field"}), 400

    result = cursor.execute("""
        SELECT * FROM Companies
        WHERE company_name=%s""",
                            [company_name])
    result = cursor.fetchone()
    if result:
        return jsonify({"message": 'company already exists'}), 400

    try:
        cursor.execute(
            """
            INSERT INTO Companies
            (company_name)
            VALUES(%s);
            """,
            [company_name]
        )
        conn.commit()

        return jsonify({"message": f"{company_name} has been added to the Companies table."}), 200

    except:
        cursor.rollback()
        return jsonify({"message": "Company could not be added"}), 404


def companies_get():
    try:
        cursor.execute(
            """
            SELECT *
            FROM Companies;
            """
        )
        result = cursor.fetchall()
        if result:
            return jsonify(({"message": "companies found", "result": result})), 200
        else:
            return jsonify(({"message": f"No companies found"})), 404
    except:
        return jsonify({"message": "Could not fetch companies data"}), 404


# def products_get():
#     return jsonify({"message": "products found", "results": product_records}), 200


# def products_get_active():
#     active_products = []
#     for product in product_records:
#         if product['active'] == True:
#             active_products.append(product)
#     if active_products:
#         return jsonify({"message": "active products found", "results": active_products}), 200
#     else:
#         return jsonify("message: no active Products were found."), 404


# def product_get_by_id(product_id):
#     for product in product_records:
#         if product['product_id'] == int(product_id):
#             return jsonify({"message": "products found", "results": product}), 200
#     return jsonify({"message": f'product with id {product_id} not found.'}), 404


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
