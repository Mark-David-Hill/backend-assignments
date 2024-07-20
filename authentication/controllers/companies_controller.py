from flask import jsonify, request

from db import db
from models.companies import Companies, companies_schema, company_schema
from util.reflection import populate_object
from lib.authenticate import auth, has_admin_permissions


@has_admin_permissions
def company_add(req):
    post_data = req.form if req.form else req.json

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    try:
        db.session.add(new_company)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201


@auth
def companies_get_all():
    companies_query = db.session.query(Companies).all()

    if len(companies_query) == 0:
        return jsonify({"message": "no companies were found"}), 404

    return jsonify({"message": "companies found", "results": companies_schema.dump(companies_query)}), 200


@auth
def company_get_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": f"company does not exist"}), 404

    return jsonify({"message": "company found", "result": company_schema.dump(company_query)}), 200


@has_admin_permissions
def company_update(req, company_id):
    post_data = req.form if req.form else req.json

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    populate_object(company_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "company updated", "result": company_schema.dump(company_query)}), 200


@has_admin_permissions
def company_delete(request, company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": f"company with id {company_id} does not exist"}), 404

    try:
        db.session.delete(company_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete"}), 400

    return jsonify({"message": f"company with id {company_id} deleted", "deleted company": company_schema.dump(company_query)}), 200
