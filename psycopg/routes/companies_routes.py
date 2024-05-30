from flask import request, Blueprint

import controllers


company = Blueprint('company', __name__)


@company.route('/company', methods=['POST'])
def company_create():
    return controllers.company_create(request)


@company.route('/companies', methods=['GET'])
def companies_get():
    return controllers.companys_get()


@company.route('/company/<company_id>', methods=['GET'])
def company_get_by_id(company_id):
    return controllers.company_get_by_id(company_id)


# @product.route('/product/<product_id>', methods=['PUT'])
# def product_update_by_id(product_id):
#     return controllers.product_update_by_id(request, product_id)


# @product.route('/product/activity/<product_id>', methods=['PATCH'])
# def product_update_active_status(product_id):
#     return controllers.product_update_active_status(product_id)


# @product.route('/product/delete/<product_id>', methods=['DELETE'])
# def product_delete(product_id):
#     return controllers.product_delete(product_id)
