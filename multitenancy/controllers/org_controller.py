from flask import jsonify

from db import db
from models.organizations import Organizations, org_schema, orgs_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def add_org(request):
  post_data = request.form if request.form else request.json

  new_org = Organizations.new_org_obj()

  populate_object(new_org, post_data)

  db.session.add(new_org)
  db.session.commit()

  return jsonify({"message": "org added", "results": org_schema.dump(new_org)})