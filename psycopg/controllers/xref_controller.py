import os

from flask import jsonify
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def xref_create(request):
    post_data = request.form if request.form else request.json
    product_id = post_data['product_id']
    category_id = post_data['category_id']

    try:
        cursor.execute(
            """
            INSERT INTO ProductsCategoriesXref
            (product_id, category_id)
            VALUES(%s, %s);
            """,
            [product_id, category_id]
        )
        conn.commit()

        return jsonify({"message": f"Xref for product id {product_id} and category id {category_id} has been added to the ProductsCategoriesXref table."}), 200

    except:
        return jsonify({"message": "Xref could not be added"}), 404
