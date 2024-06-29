from flask import Blueprint, request

import controllers

users = Blueprint('user', __name__)


@users.route("/user", methods=['POST'])
def user_add():
    return controllers.user_add(request)
