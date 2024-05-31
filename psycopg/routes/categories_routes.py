from flask import request, Blueprint

import controllers


category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def category_create():
    return controllers.category_create(request)


@category.route('/categories', methods=['GET'])
def categories_get():
    return controllers.categories_get()


@category.route('/category/<category_id>', methods=['GET'])
def category_get_by_id(category_id):
    return controllers.category_get_by_id(category_id)


@category.route('/category/<category_id>', methods=['PUT'])
def category_update_by_id(category_id):
    return controllers.category_update_by_id(request, category_id)


# @product.route('/product/delete/<product_id>', methods=['DELETE'])
# def product_delete(product_id):
#     return controllers.product_delete(product_id)
