from flask import jsonify

from data import product_records


def product_create(request):
    data = request.form if request.form else request.json
    product = {}
    product['product_id'] = data['product_id']
    product['name'] = data['name']
    product['description'] = data['description']
    product['price'] = data['price']
    product_records.append(product)
    return jsonify({"message": f"Product {product['name']} has been added."}), 200


def product_get_by_id(product_id):
    for product in product_records:
        if product['product_id'] == int(product_id):
            return jsonify({"message": "products found", "results": product}), 200
    return jsonify({"message": f'Product with id {product_id} not found.'}), 404


def product_update_by_id(request, product_id):
    data = request.form if request.form else request.json
    product = {}
    product['product_id'] = int(product_id)

    if not product['product_id']:
        return jsonify({"message": 'product_id is required'}), 400

    for record in product_records:
        print("record: ", record)
        if record['product_id'] == product['product_id']:
            product = record

    print("product: ", product)

    product['name'] = data.get('name', product['name'])
    product['description'] = data.get('description', product['description'])
    product['price'] = data.get('price', product['price'])
    product_records.append(product)

    return jsonify({"message": f"Product {product['name']} has been updated."}), 200
