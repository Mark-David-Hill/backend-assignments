from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.app_users import AppUsers, app_user_schema, app_users_schema
from util.reflection import populate_object
from lib.authenticate import auth


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
        return jsonify({"message": "user created", "result": app_user_schema.dump(new_user)}), 201


@auth
def user_get_by_id(user_id):
    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user does not exist"}), 404

    return jsonify({"message": "user found", "result": app_user_schema.dump(user_query)}), 200