from flask import request, Blueprint

from controllers import products_controller


product = Blueprint('product', __name__)


@product.route('/product', methods=['POST'])
def product_create():
    return products_controller.product_create(request)


@product.route('/product/<product_id>', methods=['GET'])
def product_get_by_id(product_id):
    return products_controller.product_get_by_id(product_id)


@product.route('/product/<product_id>', methods=['PUT'])
def product_update_by_id(product_id):
    return products_controller.product_update_by_id(request, product_id)
