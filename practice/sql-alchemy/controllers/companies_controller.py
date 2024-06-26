from flask import jsonify

from db import db
from models.companies import Companies


def company_add(req):
    post_data = req.form if req.form else req.json

    fields = ['company_name']
    required_fields = ['company_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_company = Companies(**values)

    try:
        db.session.add(new_company)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    company = {
        "company_id": new_company.company_id,
        "company_name": new_company.company_name
    }

    return jsonify({"message": "company created", "result": company}), 201


def companies_get_all():
    companies_query = db.session.query(Companies).all()

    companies_list = []

    for company in companies_query:
        company_dict = {
            'company_id': company.company_id,
            'company_name': company.company_name
        }

        companies_list.append(company_dict)

    if len(companies_list) == 0:
        return jsonify({"message": "no companies were found"}), 404

    return jsonify({"message": "companies found", "results": companies_list}), 200


def company_get_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": f"company does not exist"}), 404

    company = {
        'company_id': company_query.company_id,
        'company_name': company_query.company_name
    }

    return jsonify({"message": "company found", "result": company}), 200


def company_update(req, company_id):
    post_data = req.form if req.form else req.json

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    company_query.company_name = post_data.get("company_name", company_query)

    company = {
        "company_id": company_query.company_id,
        "company_name": company_query.company_name
    }

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "company updated", "result": company}), 200


def company_delete(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": f"company with id {company_id} does not exist"}), 404

    try:
        db.session.delete(company_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete company"}), 400

    return jsonify({"message": f"company with id {company_id} deleted"}), 200
