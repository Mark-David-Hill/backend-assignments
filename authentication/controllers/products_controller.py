from flask import jsonify, request

from db import db
from models.products import Products, products_schema, product_schema
from models.categories import Categories
from models.warranties import Warranties
from util.reflection import populate_object
from lib.authenticate import auth, has_admin_permissions


@auth
def product_add(request):
    post_data = request.form if request.form else request.json

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "product created", "result": product_schema.dump(new_product)}), 201


@auth
def product_category_update(request):
    post_data = request.form if request.form else request.json

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if product_query:
        if category_query:
            category_ids = []
            for category in product_query.categories:
                category_ids.append(str(category.category_id))

            if category_id in category_ids:
                product_query.categories.remove(category_query)
            else:
                product_query.categories.append(category_query)

            db.session.commit()

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    return jsonify({"message": "product added to category", "result": product_schema.dump(product_query)}), 200


@auth
def products_get_all():
    products_query = db.session.query(Products).all()

    if len(products_query) == 0:
        return jsonify({"message": "no products were found"}), 404

    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200


@auth
def products_get_active():
    products_query = db.session.query(Products).filter(Products.active == True).all()

    if len(products_query) == 0:
        return jsonify({"message": "no products were found"}), 404

    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200


@auth
def products_get_by_company_id(company_id):
    products_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    if len(products_query) == 0:
        return jsonify({"message": "no products were found"}), 404

    return jsonify({"message": "products found", "results": products_schema.dump(products_query)}), 200


@auth
def product_get_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    return jsonify({"message": "product found", "results": product_schema.dump(product_query)}), 200


@auth
def product_update_by_id(req, product_id):
    post_data = req.form if req.form else req.json

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    populate_object(product_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "product updated", "result": product_schema.dump(product_query)}), 200


@has_admin_permissions
def product_delete(request, product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": f"product with id {product_id} does not exist"}), 404

    try:
        db.session.delete(product_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete"}), 400

    return jsonify({"message": f"product with id {product_id} deleted", "deleted product": product_schema.dump(product_query)}), 200
