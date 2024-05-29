from flask import request, Blueprint

import controllers


category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def category_create():
    return controllers.category_create(request)


@category.route('/categories', methods=['GET'])
def categories_get():
    return controllers.categories_get()
# @product.route('/products', methods=['GET'])
# def products_get():
#     return controllers.products_get()


# @product.route('/products/active', methods=['GET'])
# def products_get_active():
#     return controllers.products_get_active()


# @product.route('/product/<product_id>', methods=['GET'])
# def product_get_by_id(product_id):
#     return controllers.product_get_by_id(product_id)


# @product.route('/product/<product_id>', methods=['PUT'])
# def product_update_by_id(product_id):
#     return controllers.product_update_by_id(request, product_id)


# @product.route('/product/activity/<product_id>', methods=['PATCH'])
# def product_update_active_status(product_id):
#     return controllers.product_update_active_status(product_id)


# @product.route('/product/delete/<product_id>', methods=['DELETE'])
# def product_delete(product_id):
#     return controllers.product_delete(product_id)
