from flask import jsonify

from db import db
from models.products import Products
from models.categories import Categories
from models.warranties import Warranties


def product_add(request):
    post_data = request.form if request.form else request.json

    fields = ['product_name', 'description', 'price', 'company_id', 'active']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        values[field] = field_data

    new_product = Products(values['product_name'], values['description'], values['price'], values['company_id'], values['active'])

    db.session.add(new_product)
    db.session.commit()

    company_dict = {
        'company_id': new_product.company.company_id,
        'company_name': new_product.company.company_name
    }

    product_dict = {
        'product_id': new_product.product_id,
        'product_name': new_product.product_name,
        'description': new_product.description,
        'price': new_product.price,
        'active': new_product.active,
        'company': company_dict
    }

    return jsonify({"message": "product created", "result": product_dict}), 201


def product_category_add(request):
    post_data = request.form if request.form else request.json

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if product_query:
        if category_query:
            product_query.categories.append(category_query)

            db.session.commit()

        categories_list = []

        for category in product_query.categories:
            categories_list.append({
                'category_id': category.category_id,
                'category_name': category.category_name
            })

    company_dict = {
        'company_id': product_query.company.company_id,
        'company_name': product_query.company.company_name
    }

    product_dict = {
        'product_id': product_query.product_id,
        'product_name': product_query.product_name,
        'description': product_query.description,
        'price': product_query.price,
        'active': product_query.active,
        'company': company_dict,
        'categories': categories_list
    }

    return jsonify({"message": "product added to category", "result": product_dict}), 200


def product_category_remove(request):
    post_data = request.form if request.form else request.json

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if product_query:
        if category_query:
            try:
                product_query.categories.remove(category_query)

                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({"message": "unable to remove product category"}), 400

            return jsonify({"message": f"category with id {category_id} removed from product with id {product_id}"}), 200
        else:
            return jsonify({"message": f"category with id {category_id} could not be found"}), 404
    else:
        return jsonify({"message": f"product with id {product_id} could not be found"}), 404


def products_get_all():
    products_query = db.session.query(Products).all()

    products_list = []

    for product in products_query:
        category_list = []

        for category in product.categories:
            category_list.append({
                'category_id': category.category_id,
                'category_name': category.category_name
            })

        company_dict = {
            'company_id': product.company.company_id,
            'company_name': product.company.company_name
        }

        if product.warranty:
            warranty_dict = {
                'warranty_id': product.warranty.warranty_id,
                'warranty_months': product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'price': product.price,
            'description': product.description,
            'active': product.active,
            'company': company_dict,
            'warranty': warranty_dict,
            'categories': category_list
        }

        products_list.append(product_dict)

    if len(products_list) == 0:
        return jsonify({"message": "no products were found"}), 404

    return jsonify({"message": "products found", "results": products_list}), 200


def products_get_active():
    products_query = db.session.query(Products).filter(Products.active == True).all()

    products_list = []

    for product in products_query:
        category_list = []

        for category in product.categories:
            category_list.append({
                'category_id': category.category_id,
                'category_name': category.category_name
            })

        company_dict = {
            'company_id': product.company.company_id,
            'company_name': product.company.company_name
        }

        if product.warranty:
            warranty_dict = {
                'warranty_id': product.warranty.warranty_id,
                'warranty_months': product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'price': product.price,
            'description': product.description,
            'active': product.active,
            'company': company_dict,
            'warranty': warranty_dict,
            'categories': category_list
        }

        products_list.append(product_dict)

    if len(products_list) == 0:
        return jsonify({"message": "no products were found"}), 404

    return jsonify({"message": "products found", "results": products_list}), 200


def products_get_by_company_id(company_id):
    products_query = db.session.query(Products).filter(Products.company_id == company_id).all()

    products_list = []

    for product in products_query:
        category_list = []

        for category in product.categories:
            category_list.append({
                'category_id': category.category_id,
                'category_name': category.category_name
            })

        company_dict = {
            'company_id': product.company.company_id,
            'company_name': product.company.company_name
        }

        if product.warranty:
            warranty_dict = {
                'warranty_id': product.warranty.warranty_id,
                'warranty_months': product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'price': product.price,
            'description': product.description,
            'active': product.active,
            'company': company_dict,
            'warranty': warranty_dict,
            'categories': category_list
        }

        products_list.append(product_dict)

    if len(products_list) == 0:
        return jsonify({"message": "no products were found"}), 404

    return jsonify({"message": "products found", "results": products_list}), 200


def product_get_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404

    category_list = []

    for category in product_query.categories:
        category_list.append({
            'category_id': category.category_id,
            'category_name': category.category_name
        })

    company_dict = {
        'company_id': product_query.company.company_id,
        'company_name': product_query.company.company_name
    }

    if product_query.warranty:
        warranty_dict = {
            'warranty_id': product_query.warranty.warranty_id,
            'warranty_months': product_query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product_dict = {
        'product_id': product_query.product_id,
        'product_name': product_query.product_name,
        'description': product_query.description,
        'price': product_query.price,
        'active': product_query.active,
        'company': company_dict,
        'warranty': warranty_dict,
        'categories': category_list
    }

    return jsonify({"message": "product found", "results": product_dict}), 200


def product_update_by_id(req, product_id):
    post_data = req.form if req.form else req.json

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    product_query.product_name = post_data.get("product_name", product_query)
    product_query.price = post_data.get("price", product_query)
    product_query.description = post_data.get("description", product_query)

    company_dict = {
        'company_id': product_query.company.company_id,
        'company_name': product_query.company.company_name
    }

    product_dict = {
        'product_id': product_query.product_id,
        'product_name': product_query.product_name,
        'description': product_query.description,
        'price': product_query.price,
        'active': product_query.active,
        'company': company_dict
    }

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "product updated", "result": product_dict}), 200


def product_delete(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": f"product with id {product_id} does not exist"}), 404

    try:
        db.session.delete(product_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete"}), 400

    return jsonify({"message": f"product with id {product_id} deleted"}), 200
