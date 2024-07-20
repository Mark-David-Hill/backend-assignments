from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.app_users import AppUsers, app_user_schema, app_users_schema
from util.reflection import populate_object
from lib.authenticate import auth, has_admin_permissions


@auth
def user_add(req):
    post_data = req.form if req.form else req.json

    new_user = AppUsers.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "unable to create user"}), 400

    return jsonify({"message": "user created", "result": app_user_schema.dump(new_user)}), 201


@auth
def users_get_all():
    users_query = db.session.query(AppUsers).all()

    if len(users_query) == 0:
        return jsonify({"message": "no users were found"}), 404

    return jsonify({"message": "users found", "results": app_users_schema.dump(users_query)}), 200


@auth
def user_get_by_id(user_id):
    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": f"user does not exist"}), 404

    return jsonify({"message": "user found", "result": app_user_schema.dump(user_query)}), 200


@auth
def user_update(req, user_id):
    post_data = req.form if req.form else req.json

    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    populate_object(user_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "user updated", "result": app_user_schema.dump(user_query)}), 200


@has_admin_permissions
def user_delete(user_id):
    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": f"user with id {user_id} does not exist"}), 404

    try:
        db.session.delete(user_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete"}), 400

    return jsonify({"message": f"user with id {user_id} deleted", "deleted user": app_user_schema.dump(user_query)}), 200
