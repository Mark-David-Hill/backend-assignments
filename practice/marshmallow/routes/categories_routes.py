from flask import request, Blueprint

import controllers
# from controllers import categories_controller

categories = Blueprint('categories', __name__)


@categories.route('/category', methods=["POST"])
def categories_add():
    return controllers.categories_controller.category_add(request)


@categories.route('/categories')
def categories_get_all():
    return controllers.categories_controller.categories_get_all()


@categories.route('/category/<category_id>')
def category_get_by_id(category_id):
    return controllers.categories_controller.category_get_by_id(category_id)


@categories.route('/category/<category_id>', methods=["PUT"])
def category_update(category_id):
    return controllers.categories_controller.category_update(request, category_id)


@categories.route('/category/delete/<category_id>', methods=["DELETE"])
def category_delete(category_id):
    return controllers.categories_controller.category_delete(category_id)
