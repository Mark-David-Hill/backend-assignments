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

    if not product_id or not warranty_months:
        return jsonify({"message": "product_id and warranty_months are both required fields"}), 400

    cursor.execute("""
        SELECT * FROM Warranties
        WHERE product_id=%s""",
                   [product_id])
    result = cursor.fetchone()
    if result:
        return jsonify({"message": f'warranty for product id {product_id} already exists'}), 400

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

        cursor.execute(
            """
            SELECT *
            FROM Warranties
            ORDER BY warranty_id DESC;
            """
        )
        result = cursor.fetchone()

        if result:
            warranty_list = []

            warranty_record = {
                'warranty_id': result[0],
                'product_id': result[1],
                'warranty_months': result[2]
            }

            warranty_list.append(warranty_record)

        return jsonify({"message": f"Warranty for product with id {product_id} has been added to the Warranties table.", "result": warranty_list}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Warranty could not be added"}), 404


def warranties_get():
    try:
        cursor.execute(
            """
            SELECT *
            FROM Warranties;
            """
        )
        results = cursor.fetchall()

        if results:
            warranty_list = []

            for warranty in results:
                warranty_record = {
                    'warranty_id': warranty[0],
                    'product_id': warranty[1],
                    'warranty_months': warranty[2]
                }

                warranty_list.append(warranty_record)

            return jsonify(({"message": "Warranties found", "results": warranty_list})), 200
        else:
            return jsonify(({"message": f"No warranties found"})), 404
    except Exception as e:
        print(e)
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
            warranty_list = []

            warranty_record = {
                'warranty_id': result[0],
                'product_id': result[1],
                'warranty_months': result[2]
            }

            warranty_list.append(warranty_record)

            return jsonify(({"message": f"warranty with id {warranty_id} found", "result": warranty_list})), 200
        else:
            return jsonify(({"message": "No warranty found"})), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Could not fetch warranty data"}), 404


def warranty_update_by_id(request, warranty_id):
    post_data = request.form if request.form else request.json
    warranty_months = post_data['warranty_months']

    if not warranty_months:
        return jsonify({"message": "warranty_months is a Required Field"}), 400

    try:
        cursor.execute("""
            UPDATE Warranties
            SET warranty_months=%s
            WHERE warranty_id=%s""",
                       [warranty_months, warranty_id])
        conn.commit()

        cursor.execute(
            """
            SELECT *
            FROM Warranties
            WHERE warranty_id=%s;
            """, [warranty_id]
        )
        result = cursor.fetchone()

        if result:
            warranty_list = []

            warranty_record = {
                'warranty_id': result[0],
                'product_id': result[1],
                'warranty_months': result[2]
            }

            warranty_list.append(warranty_record)
            return jsonify(({"message": f"warranty with id {warranty_id} has been updated", "result": warranty_list})), 200
        else:
            return jsonify(({"message": "No warranty found"})), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "Warranty could not be updated"}), 404


def warranty_delete(warranty_id):
    warranty = {}
    warranty['warranty_id'] = int(warranty_id)

    if not warranty['warranty_id']:
        return jsonify({"message": 'warranty_id is required'}), 400

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
            cursor.execute("""
                DELETE FROM Warranties
                WHERE warranty_id=%s
                """, [warranty_id])
            conn.commit()

            return jsonify({"message": f"warranty with id {warranty_id} and its associated product have been deleted."}), 200
        else:
            return jsonify({"message": f"no warranty exists with id {warranty_id}"}), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "warranty could not be deleted"}), 404
