from flask import request, Blueprint

from controllers import warranties_controller

warranties = Blueprint('warranties', __name__)


@warranties.route('/warranty', methods=['POST'])
def warranty_add():
    return warranties_controller.warranty_add(request)


@warranties.route('/warranty/category', methods=['POST'])
def warranty_category_add():
    return warranties_controller.warranty_category_add(request)


@warranties.route('/warranty/<warranty_id>')
def warranties_get_by_id(warranty_id):
    return warranties_controller.warranty_get_by_id(warranty_id)
