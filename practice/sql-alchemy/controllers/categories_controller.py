from flask import jsonify

from db import db
from models.categories import Categories


def category_add(req):
    post_data = req.form if req.form else req.json

    fields = ['category_name']
    required_fields = ['category_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_category = Categories(**values)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    print("NEW CATEGORY: ", new_category)

    category = {
        "category_id": new_category.category_id,
        "category_name": new_category.category_name
    }

    return jsonify({"message": "category created", "result": category}), 201


def categories_get_all():
    categories_query = db.session.query(Categories).all()

    categories_list = []

    for category in categories_query:
        category_dict = {
            'category_id': category.category_id,
            'category_name': category.category_name
        }

        categories_list.append(category_dict)

    if len(categories_list) == 0:
        return jsonify({"message": "no categories were found"}), 404

    return jsonify({"message": "categories found", "results": categories_list}), 200


def category_get_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": f"category does not exist"}), 404

    category = {
        'category_id': category_query.category_id,
        'category_name': category_query.category_name
    }

    return jsonify({"message": "category found", "result": category}), 200


def category_update(req, category_id):
    post_data = req.form if req.form else req.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    category_query.category_name = post_data.get("category_name", category_query)

    category = {
        "category_id": category_query.category_id,
        "category_name": category_query.category_name
    }

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "category updated", "result": category}), 200


def category_delete(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": f"category with id {category_id} does not exist"}), 404

    try:
        db.session.delete(category_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete category"}), 400

    return jsonify({"message": f"category with id {category_id} deleted"}), 200
