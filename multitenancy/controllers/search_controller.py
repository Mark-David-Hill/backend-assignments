from flask import jsonify
from sqlalchemy import func

from db import db
from models.app_users import AppUsers, users_schema
from models.organizations import Organizations, orgs_schema
from lib.authenticate import authenticate


@authenticate
def users_get_by_search(request):
    search_term = request.args.get('q').lower()

    user_data = db.session.query(AppUsers).filter(db.or_(db.func.lower(AppUsers.first_name).contains(search_term), db.func.lower(AppUsers.last_name).contains(search_term), db.func.lower(AppUsers.email).contains(search_term))).order_by(AppUsers.last_name.asc())

    return jsonify({"message": "users found", "results": users_schema.dump(user_data)}), 200


@authenticate
def orgs_get_by_search(request):
    search_term = request.args.get('q').lower()

    org_data = db.session.query(Organizations).filter(db.or_(db.func.lower(Organizations.name).contains(search_term), db.func.lower(Organizations.email).contains(search_term))).order_by(Organizations.name.asc())

    return jsonify({"message": "organizations found", "results": orgs_schema.dump(org_data)}), 200
