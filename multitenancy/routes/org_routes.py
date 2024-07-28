from flask import Blueprint, request

import controllers

orgs = Blueprint('orgs', __name__)


@orgs.route('/org', methods=['POST'])
def add_org():
  return controllers.add_org(request)

