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
        return jsonify({"message": f'Category with name {category_name} already exists'}), 400

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

        cursor.execute(
            """
            SELECT *
            FROM Categories
            ORDER BY category_id DESC;
            """
        )
        result = cursor.fetchone()
        if result:
            category_list = []

            category_record = {
                'category_id': result[0],
                'category_name': result[1]
            }

            category_list.append(category_record)

        return jsonify({"message": f"{category_name} has been added to the Categories table.", "result": category_list}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Product could not be added"}), 404


def categories_get():
    try:
        cursor.execute(
            """
            SELECT *
            FROM Categories;
            """
        )
        results = cursor.fetchall()
        if results:
            category_list = []

            for category in results:
                category_record = {
                    'category_id': category[0],
                    'category_name': category[1]
                }

                category_list.append(category_record)

            return jsonify(({"message": "Categories found", "results": category_list})), 200
        else:
            return jsonify(({"message": f"No categories found"})), 404
    except Exception as e:
        print(e)
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
            category_list = []

            category_record = {
                'category_id': result[0],
                'category_name': result[1]
            }

            category_list.append(category_record)

            return jsonify(({"message": f"category with id {category_id} found", "result": category_list})), 200
        else:
            return jsonify(({"message": "No category found"})), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Could not fetch category data"}), 404


def category_update_by_id(request, category_id):
    post_data = request.form if request.form else request.json
    category_name = post_data['category_name']

    if not category_name:
        return jsonify({"message": "category_name is a Required Field"}), 400

    try:
        cursor.execute("""
            UPDATE Categories
            SET category_name=%s
            WHERE category_id=%s""",
                       [category_name, category_id])
        conn.commit()

        cursor.execute(
            """
                SELECT *
                FROM Categories
                WHERE category_id=%s;
                """, [category_id]
        )
        result = cursor.fetchone()

        if result:
            category_list = []

            category_record = {
                'category_id': result[0],
                'category_name': result[1]
            }

            category_list.append(category_record)
            return jsonify(({"message": f"{category_name} has been updated", "result": category_list})), 200
        else:
            return jsonify(({"message": "No category found"})), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "Category could not be updated"}), 404


def category_delete(category_id):
    category = {}
    category['category_id'] = int(category_id)

    if not category['category_id']:
        return jsonify({"message": 'category_id is required'}), 400

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
            cursor.execute("""
                DELETE FROM Categories
                WHERE category_id=%s
                """, [category_id])
            conn.commit()

            return jsonify({"message": f"category with id {category_id} has been deleted."}), 200
        else:
            return jsonify({"message": f"no category exists with id {category_id}"}), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "category could not be deleted"}), 404
