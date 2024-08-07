from flask import request, Blueprint

import controllers

warranties = Blueprint('warranties', __name__)


@warranties.route('/warranty', methods=["POST"])
def warranties_add():
    return controllers.warranties_controller.warranty_add(request)


@warranties.route('/warranties')
def warranties_get_all():
    return controllers.warranties_controller.warranties_get_all()


@warranties.route('/warranty/<warranty_id>')
def warranty_get_by_id(warranty_id):
    return controllers.warranties_controller.warranty_get_by_id(warranty_id)


@warranties.route('/warranty/<warranty_id>', methods=["PUT"])
def warranty_update(warranty_id):
    return controllers.warranties_controller.warranty_update(request, warranty_id)


@warranties.route('/warranty/delete/<warranty_id>', methods=["DELETE"])
def warranty_delete(warranty_id):
    return controllers.warranties_controller.warranty_delete(request, warranty_id)
