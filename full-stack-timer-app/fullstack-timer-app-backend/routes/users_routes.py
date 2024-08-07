from flask import Blueprint, request

import controllers

users = Blueprint("user", __name__)


@users.route("/user", methods=["POST"])
def user_add():
    return controllers.user_add(request)


@users.route("/user/<user_id>")
def user_get_by_id(user_id):
    return controllers.user_update(request, user_id)