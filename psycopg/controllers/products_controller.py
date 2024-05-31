import os

from flask import jsonify
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def find_dict_index(list, key, value):
    for index, dictionary in enumerate(list):
        if dictionary.get(key) == value:
            return index
    return -1


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

        cursor.execute(
            """
            SELECT COUNT(*) 
            FROM Products
            """
        )
        print('after execute')
        product_id = cursor.fetchone()[0]
        print("product id:", product_id)
        print("result:", result)

        product_list = []
        product_record = {
            'product_id': product_id,
            'company_id': company_id,
            'product_name': product_name,
            'price': price,
            'description': description
        }
        print("before append")
        product_list.append(product_record)

    except:
        return jsonify({"message": "Product could not be added"}), 404

    return jsonify({"message": f"{product_name} has been added to the Products table.", "result": product_list}), 200


def products_get():

    try:
        cursor.execute(
            """
            SELECT p.product_id, p.product_name, p.price, p.description, c.category_name, w.warranty_months
            FROM Products p
            INNER JOIN ProductsCategoriesXref x ON (p.product_id = x.product_id)
            INNER JOIN Categories c ON (x.category_id = c.category_id)
            INNER JOIN Warranties w ON (p.product_id = w.product_id)
            """
        )
        results = cursor.fetchall()

        if results:
            product_list = []

            for product in results:
                dict_id = find_dict_index(product_list, 'product_id', product[0])

                if dict_id != -1:
                    current_category_name = product_list[dict_id]['category_name']
                    new_category_name = product[4]

                    product_list[dict_id]['category_name'] = current_category_name + ", " + new_category_name

                else:
                    product_record = {
                        'product_id': product[0],
                        'product_name': product[1],
                        'price': product[2],
                        'description': product[3],
                        'category_name': product[4],
                        'warranty_months': product[5]
                    }

                    product_list.append(product_record)

            return jsonify(({"message": "products found", "results": product_list})), 200
        else:
            return jsonify(({"message": f"No products found"})), 404
    except:
        return jsonify({"message": "Could not fetch products data"}), 404


def products_get_active():
    try:
        cursor.execute(
            """
            SELECT p.product_id, p.product_name, p.price, p.description, c.category_name, w.warranty_months
            FROM Products p
            INNER JOIN ProductsCategoriesXref x ON (p.product_id = x.product_id)
            INNER JOIN Categories c ON (x.category_id = c.category_id)
            INNER JOIN Warranties w ON (p.product_id = w.product_id)
            WHERE p.active=True
            """,
        )
        results = cursor.fetchall()

        if results:
            product_list = []

            for product in results:
                dict_id = find_dict_index(product_list, 'product_id', product[0])

                if dict_id != -1:
                    current_category_name = product_list[dict_id]['category_name']
                    new_category_name = product[4]

                    product_list[dict_id]['category_name'] = current_category_name + ", " + new_category_name

                else:
                    product_record = {
                        'product_id': product[0],
                        'product_name': product[1],
                        'price': product[2],
                        'description': product[3],
                        'category_name': product[4],
                        'warranty_months': product[5]
                    }

                    product_list.append(product_record)

            return jsonify(({"message": "active products found", "results": product_list})), 200
        else:
            return jsonify(({"message": f"No active products found"})), 404
    except:
        return jsonify({"message": "Could not fetch products data"}), 404


def product_get_by_id(product_id):
    try:
        cursor.execute(
            """
            SELECT p.product_id, p.product_name, p.price, p.description, c.category_name, w.warranty_months
            FROM Products p
            INNER JOIN ProductsCategoriesXref x ON (p.product_id = x.product_id)
            INNER JOIN Categories c ON (x.category_id = c.category_id)
            INNER JOIN Warranties w ON (p.product_id = w.product_id)
            WHERE p.product_id=%s
            """, [product_id]
        )
        results = cursor.fetchall()

        if results:
            product_list = []

            for product in results:
                dict_id = find_dict_index(product_list, 'product_id', product[0])

                if dict_id != -1:
                    current_category_name = product_list[dict_id]['category_name']
                    new_category_name = product[4]

                    product_list[dict_id]['category_name'] = current_category_name + ", " + new_category_name

                else:
                    product_record = {
                        'product_id': product[0],
                        'product_name': product[1],
                        'price': product[2],
                        'description': product[3],
                        'category_name': product[4],
                        'warranty_months': product[5]
                    }

                    product_list.append(product_record)

            return jsonify(({"message": "product found", "results": product_list})), 200
        else:
            return jsonify(({f"message": f"No product found with id {product_id}"})), 404
    except:
        return jsonify({"message": "Could not fetch product data"}), 404


def product_update_by_id(request, product_id):
    post_data = request.form if request.form else request.json
    product_name = post_data['product_name']
    price = post_data['price']
    description = post_data['description']

    if not product_name:
        return jsonify({"message": "product_name is a Required Field"}), 400

    try:
        cursor.execute("""
            UPDATE Products
            SET product_name=%s,
                       price=%s,
                       description=%s
            WHERE product_id=%s""",
                       [product_name, price, description, product_id])
        conn.commit()

    except:
        return jsonify({"message": "Product has been updated"}), 404

    return jsonify({"message": f"{product_name} has been updated."}), 200


def product_update_active_status(request, product_id):
    post_data = request.form if request.form else request.json
    active = post_data['active']

    if not active:
        return jsonify({"message": "active is a Required Field"}), 400

    try:
        cursor.execute("""
            UPDATE Products
            SET active=%s
            WHERE product_id=%s"""
                       [active, product_id])
        conn.commit()

    except:
        return jsonify({"message": "Product has been updated"}), 404

    return jsonify({"message": f"Product ID {product_id}'s active status has been updated."}), 200


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
