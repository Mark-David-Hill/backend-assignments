from flask import jsonify
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta

from db import db
from models.app_users import AppUsers
from models.auth_tokens import AuthTokens, auth_token_schema
from lib.authenticate import auth


def auth_token_add(req):
    post_data = req.form if req.form else req.json

    email = post_data.get("email")
    password = post_data.get("password")

    if email and password:
        user_data = db.session.query(AppUsers).filter(AppUsers.email == post_data.get('email')).first()

        if user_data:
            valid_password = check_password_hash(user_data.password, password)

            if not valid_password:
                return jsonify({"message": "invalid login"}), 401

            existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_data.user_id).all()

            if existing_tokens:
                for token in existing_tokens:
                    if token.expiration < datetime.now():
                        db.session.delete(token)

            expiry = datetime.now() + timedelta(hours=12)

            new_token = AuthTokens(user_data.user_id, expiry)
            db.session.add(new_token)
            db.session.commit()

        else:
            return jsonify({"message": "no user data found"}), 404

        return jsonify({"message": "authorization successful", "result": auth_token_schema.dump(new_token)}), 201


@auth
def logout(req):
    post_data = req.form if req.form else req.json
    print("POST DATA:", post_data)
    user_id = post_data.get('user_id')
    print("USER ID", user_id)

    if not user_id:
        return jsonify({"message": "user_id is a required field"})

    existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).all()

    if existing_tokens:
        try:
            for token in existing_tokens:
                db.session.delete(token)

            db.session.commit()
            return ({"message": f"user with id {user_id} has been logged out"})
        except:
            db.session.rollback()
            return jsonify({"message": f"unable to logout user with id {user_id}"}), 400
    else:
        return jsonify({"message": f"user with id {user_id} could not be logged out because they are not authenticated"})
