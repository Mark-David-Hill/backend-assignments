from flask import jsonify

from db import db
from models.categories import Categories, categories_schema, category_schema
from util.reflection import populate_object


def category_add(req):
    post_data = req.form if req.form else req.json

    # fields = ['category_name']
    # required_fields = ['category_name']

    # values = {}

    # for field in fields:
    #     field_data = post_data.get(field)

    #     if field_data in required_fields and not field_data:
    #         return jsonify({"message": f'{field} is required'}), 400

    #     values[field] = field_data

    # new_category = Categories(**values)

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    # query = db.session.query(Categories).filter(Categories.category_name == values['category_name']).first()

    # category = {
    #     "category_id": query.category_id,
    #     "category_name": query.category_name
    # }

    return jsonify({"message": "category created", "result": category_schema.dump(new_category)}), 201


def categories_get_all():
    categories_query = db.session.query(Categories).all()

    # category_list = []

    # for category in categories_query:
    #     category_dict = {
    #         'category_id': category.category_id,
    #         'category_name': category.category_name
    #     }

    #     category_list.append(category_dict)

    # if len(category_list) == 0:
    #     return jsonify({"message": "no categories were found"}), 403

    return jsonify({"message": "categories found", "results": categories_schema.dump(categories_query)}), 200


def category_get_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": f"category does not exist"}), 404

    # category = {
    #     'category_id': category_query.category_id,
    #     'category_name': category_query.category_name
    # }

    return jsonify({"message": "category found", "result": category_schema.dump(category_query)}), 200


def category_update(req, category_id):
    post_data = req.form if req.form else req.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    populate_object(category_query, post_data)

    # category_query.category_name = post_data.get("category_name", category_query)

    # category = {
    #     "category_id": category_query.category_id,
    #     "category_name": category_query.category_name
    # }

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "category updated", "result": category_schema.dump(category_query)})


def category_delete(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": f"category with id {category_id} does not exist"}), 404

    try:
        db.session.delete(category_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete"})

    return jsonify({"message": f"category with id {category_id} deleted", "deleted category": category_schema.dump(category_query)})
