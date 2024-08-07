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
    auth_token = req.headers.get("auth")

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
    def function_wrapper(*args, **kwargs):
        auth_info = validate_token(request)

        if auth_info:
            return function(*args, **kwargs)
        else:
            return fail_response()

    return function_wrapper