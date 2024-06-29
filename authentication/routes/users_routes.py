from flask import Blueprint, request

import controllers

users = Blueprint('user', __name__)


@users.route("/user", methods=['POST'])
def user_add():
    return controllers.user_add(request)


@users.route('/users')
def users_get_all():
    return controllers.users_controller.users_get_all()


@users.route('/user/<user_id>')
def user_get_by_id(user_id):
    return controllers.users_controller.user_get_by_id(user_id)


@users.route('/user/<user_id>', methods=["PUT"])
def user_update(user_id):
    return controllers.users_controller.user_update(request, user_id)


@users.route('/user/delete/<user_id>', methods=["DELETE"])
def user_delete(user_id):
    return controllers.users_controller.user_delete(user_id)
