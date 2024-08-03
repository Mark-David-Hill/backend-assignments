from flask import request, Blueprint

import controllers

search = Blueprint('search', __name__)


@search.route('/user/search', methods=['GET'])
def users_get_by_search():
    return controllers.users_get_by_search(request)

@search.route('/org/search', methods=['GET'])
def orgs_get_by_search():
    return controllers.orgs_get_by_search(request)