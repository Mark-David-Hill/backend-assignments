from flask import jsonify

from data import product_records


def product_create(request):
    data = request.form if request.form else request.json
    product = {}
    product['product_id'] = data['product_id']
    product['product_name'] = data['product_name']
    product['description'] = data['description']
    product['price'] = data['price']
    product['active'] = bool(data['active'])
    product_records.append(product)
    return jsonify({"message": f"Product {product['product_name']} has been added."}), 200


def products_get():
    return jsonify(product_records), 200


def products_get_active():
    active_products = []
    for product in product_records:
        if product['active'] == True:
            active_products.append(product)
    if active_products:
        return jsonify(active_products), 200
    else:
        return jsonify("Message: no active Products were found."), 404


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
        if record['product_id'] == product['product_id']:
            product = record

    product['product_name'] = data.get('product_name', product['product_name'])
    product['description'] = data.get('description', product['description'])
    product['price'] = data.get('price', product['price'])
    product['active'] = data.get('active', product['active'])
    product_records.append(product)

    return jsonify({"message": f"Product {product['product_name']} has been updated."}), 200


def product_update_active_status(product_id):
    product = {}
    product['product_id'] = int(product_id)

    if not product['product_id']:
        return jsonify({"message": 'product_id is required'}), 400

    for record in product_records:
        if record['product_id'] == product['product_id']:
            product = record

    product['active'] = not product['active']
    product_records.append(product)

    return jsonify({"message": f"Product {product['product_name']}'s active status has been set to {product['active']}."}), 200


def product_delete(product_id):
    product = {}
    product['product_id'] = int(product_id)

    if not product['product_id']:
        return jsonify({"message": 'product_id is required'}), 400

    for record in product_records:
        if record['product_id'] == product['product_id']:
            product = record

    product_records.remove(product)

    return jsonify({"message": f"Product {product['product_name']} has been deleted."}), 200
