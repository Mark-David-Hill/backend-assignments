from flask import jsonify

from db import db
from models.categories import Categories, categories_schema, category_schema
from util.reflection import populate_object
from lib.authenticate import auth


@auth
def category_add(req):
    post_data = req.form if req.form else req.json

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "category created", "result": category_schema.dump(new_category)}), 201


def categories_get_all():
    categories_query = db.session.query(Categories).all()

    if len(categories_query) == 0:
        return jsonify({"message": "no categories were found"}), 404

    return jsonify({"message": "categories found", "results": categories_schema.dump(categories_query)}), 200


def category_get_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": f"category does not exist"}), 404

    return jsonify({"message": "category found", "result": category_schema.dump(category_query)}), 200


@auth
def category_update(req, category_id):
    post_data = req.form if req.form else req.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    populate_object(category_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "category updated", "result": category_schema.dump(category_query)}), 200


# @has_admin_permissions
@auth
def category_delete(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": f"category with id {category_id} does not exist"}), 404

    try:
        db.session.delete(category_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete"}), 400

    return jsonify({"message": f"category with id {category_id} deleted", "deleted category": category_schema.dump(category_query)}), 200
