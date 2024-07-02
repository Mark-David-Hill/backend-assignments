from flask import jsonify, request
import functools
from datetime import datetime
from uuid import UUID

from db import db
from models.auth_tokens import AuthTokens
from models.app_users import AppUsers


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except:
        return False


def validate_token(req):
    auth_token = req.headers.get('auth')

    if not auth_token or not validate_uuid4(auth_token):
        return False

    existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now():
            return existing_token

    else:
        return False


def fail_response():
    return jsonify({"message": "authentication required"}), 401


def auth(function):
    @functools.wraps(function)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(request)

        if auth_info:
            return function(*args, **kwargs)
        else:
            return fail_response()

    return wrapper_auth_return


def has_admin_permissions(function):
    @functools.wraps(function)
    def wrapper_has_admin_permissions_return(*args, **kwargs):
        auth_info = validate_token(request)

        if auth_info:
            user_id = auth_info.user_id

            user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
            if user_query:
                user_role = user_query.role
                if user_role == "admin":
                    return function(*args, **kwargs)
                else:
                    return jsonify({"message": "forbidden: admin permissions required"}), 403

        return fail_response()

    return wrapper_has_admin_permissions_return
