from flask import request, Blueprint

import controllers


company = Blueprint('company', __name__)


@company.route('/company', methods=['POST'])
def company_create():
    return controllers.company_create(request)


@company.route('/companies', methods=['GET'])
def companies_get():
    return controllers.companies_get()


@company.route('/company/<company_id>', methods=['GET'])
def company_get_by_id(company_id):
    return controllers.company_get_by_id(company_id)


@company.route('/company/<company_id>', methods=['PUT'])
def company_update_by_id(company_id):
    return controllers.company_update_by_id(request, company_id)


@company.route('/company/delete/<company_id>', methods=['DELETE'])
def company_delete(company_id):
    return controllers.company_delete(company_id)
