from flask import request, Blueprint

from controllers import warranties_controller

warranties = Blueprint('warranties', __name__)


@warranties.route('/warranty', methods=["POST"])
def warranties_add():
    return warranties_controller.warranty_add(request)


@warranties.route('/warranties')
def warranties_get_all():
    return warranties_controller.warranties_get_all()


@warranties.route('/warranty/<warranty_id>')
def warranty_get_by_id(warranty_id):
    return warranties_controller.warranty_get_by_id(warranty_id)


@warranties.route('/warranty/<warranty_id>', methods=["PUT"])
def warranty_update(warranty_id):
    return warranties_controller.warranty_update(request, warranty_id)


@warranties.route('/warranty/delete/<warranty_id>', methods=["DELETE"])
def warranty_delete(warranty_id):
    return warranties_controller.warranty_delete(warranty_id)
