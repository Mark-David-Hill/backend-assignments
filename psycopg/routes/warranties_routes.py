from flask import request, Blueprint

import controllers


warranty = Blueprint('warranty', __name__)


@warranty.route('/warranty', methods=['POST'])
def warranty_create():
    return controllers.warranty_create(request)


@warranty.route('/warranties', methods=['GET'])
def warranties_get():
    return controllers.warranties_get()


@warranty.route('/warranty/<warranty_id>', methods=['GET'])
def warranty_get_by_id(warranty_id):
    return controllers.warranty_get_by_id(warranty_id)


@warranty.route('/warranty/<warranty_id>', methods=['PUT'])
def warranty_update_by_id(warranty_id):
    return controllers.warranty_update_by_id(request, warranty_id)


@warranty.route('/warranty/delete/<warranty_id>', methods=['DELETE'])
def warranty_delete(warranty_id):
    return controllers.warranty_delete(warranty_id)
