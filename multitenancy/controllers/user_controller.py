from flask import jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.app_users import AppUsers, user_schema, users_schema
from models.organizations import Organizations
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth

def add_user(request):
  post_data = request.form if request.form else request.json
  org_id = post_data.get("org_id")

  new_user = AppUsers.new_user_obj()

  populate_object(new_user, post_data)

  new_user.password = generate_password_hash(new_user.password).decode('utf8')

  if org_id:
    org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

    if org_query == None:
      return jsonify({"message": "org id required"}), 400

  db.session.add(new_user)
  db.session.commit()

  return jsonify({"message": "user added", "results": user_schema.dump(new_user)}), 201


@authenticate_return_auth
def get_user_by_id(request, user_id, auth_info):
  user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

  if user_id == str(auth_info.user.user_id) or auth_info.user.role == 'super-admin':
    return jsonify({"message": "user found", "results": user_schema.dump(user_query)}), 200
  
  else:
    return jsonify({"message": "unauthorized"}), 403
  
@authenticate_return_auth
def get_all_users(request, auth_info):
  users_query = db.session.query(AppUsers).all()

  if auth_info.user.role == 'super-admin':
    return jsonify({"message": "users found", "results": users_schema.dump(users_query)}), 200

  else:
    return jsonify({"message": "unauthorized"}), 401