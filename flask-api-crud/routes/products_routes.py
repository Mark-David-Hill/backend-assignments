from flask import request, Blueprint

from controllers import products_controller


product = Blueprint('product', __name__)


@product.route('/product', methods=['POST'])
def product_create():
    return products_controller.product_create(request)


@product.route('/products', methods=['GET'])
def products_get():
    return products_controller.products_get()


@product.route('/products/active', methods=['GET'])
def products_get_active():
    return products_controller.products_get_active()


@product.route('/product/<product_id>', methods=['GET'])
def product_get_by_id(product_id):
    return products_controller.product_get_by_id(product_id)


@product.route('/product/<product_id>', methods=['PUT'])
def product_update_by_id(product_id):
    return products_controller.product_update_by_id(request, product_id)


@product.route('/product/activity/<product_id>', methods=['PUT'])
def product_update_active_status(product_id):
    return products_controller.product_update_active_status(product_id)


@product.route('/product/delete/<product_id>', methods=['DELETE'])
def product_delete(product_id):
    return products_controller.product_delete(product_id)
