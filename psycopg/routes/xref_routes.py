from flask import request, Blueprint

import controllers


xref = Blueprint('xref', __name__)


@xref.route('/xref', methods=['POST'])
def xref_create():
    return controllers.xref_create(request)
