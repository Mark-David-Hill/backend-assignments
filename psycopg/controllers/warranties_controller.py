import os

from flask import jsonify
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def warranty_create(request):
    post_data = request.form if request.form else request.json
    product_id = post_data['product_id']
    warranty_months = post_data['warranty_months']

    try:
        cursor.execute(
            """
            INSERT INTO Warranties
            (product_id, warranty_months)
            VALUES(%s, %s);
            """,
            [product_id, warranty_months]
        )
        conn.commit()

        return jsonify({"message": f"Warranty for product id {product_id} has been added to the Warranties table."}), 200

    except:
        return jsonify({"message": "Warranty could not be added"}), 404


def warranties_get():
    try:
        cursor.execute(
            """
            SELECT *
            FROM Warranties;
            """
        )
        result = cursor.fetchall()
        if result:
            return jsonify(({"message": "warranties found", "result": result})), 200
        else:
            return jsonify(({"message": f"No warranties found"})), 404
    except:
        return jsonify({"message": "Could not fetch warranties data"}), 404


def warranty_get_by_id(warranty_id):
    try:
        cursor.execute(
            """
            SELECT *
            FROM Warranties
            WHERE warranty_id=%s;
            """, [warranty_id]
        )
        result = cursor.fetchone()
        if result:
            return jsonify(({"message": f"warranty with id {warranty_id} found", "result": result})), 200
        else:
            return jsonify(({"message": "No warranty found"})), 404
    except:
        return jsonify({"message": "Could not fetch warranty data"}), 404

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
