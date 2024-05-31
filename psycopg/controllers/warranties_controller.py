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

    except:
        return jsonify({"message": "Product has been updated"}), 404

    return jsonify({"message": f"{warranty_months} has been updated."}), 200


def warranty_delete(warranty_id):
    warranty = {}
    warranty['warranty_id'] = int(warranty_id)

    if not warranty['warranty_id']:
        return jsonify({"message": 'warranty_id is required'}), 400

    try:
        cursor.execute("""
            DELETE FROM Warranties
            WHERE warranty_id=%s
            """, [warranty_id])
        conn.commit()

    except:
        return jsonify({"message": "warranty could not be deleted"}), 404

    return jsonify({"message": f"warranty with id {warranty_id} has been deleted."}), 200
