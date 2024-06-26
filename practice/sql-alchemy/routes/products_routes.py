from flask import request, Blueprint

from controllers import products_controller

products = Blueprint('products', __name__)


@products.route('/product', methods=['POST'])
def product_add():
    return products_controller.product_add(request)


@products.route('/product/category', methods=['POST'])
def product_category_add():
    return products_controller.product_category_add(request)


@products.route('/product/category/delete', methods=['DELETE'])
def product_category_remove():
    return products_controller.product_category_remove(request)


@products.route('/products')
def products_get_all():
    return products_controller.products_get_all()


@products.route('/products/active')
def products_get_active():
    return products_controller.products_get_active()


@products.route('/product/company/<company_id>')
def products_get_by_company_id(company_id):
    return products_controller.products_get_by_company_id(company_id)


@products.route('/product/<product_id>')
def products_get_by_id(product_id):
    return products_controller.product_get_by_id(product_id)


@products.route('/product/<product_id>', methods=['PUT'])
def product_update_by_id(product_id):
    return products_controller.product_update_by_id(request, product_id)


@products.route('/product/delete/<product_id>', methods=["DELETE"])
def product_delete(product_id):
    return products_controller.product_delete(product_id)
