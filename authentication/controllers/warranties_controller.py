from flask import jsonify, request

from db import db
from models.warranties import Warranties, warranties_schema, warranty_schema
from util.reflection import populate_object
from lib.authenticate import auth, has_admin_permissions


@auth
def warranty_add(req):
    post_data = req.form if req.form else req.json

    new_warranty = Warranties.new_warranty_obj()
    populate_object(new_warranty, post_data)

    try:
        db.session.add(new_warranty)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "warranty created", "result": warranty_schema.dump(new_warranty)}), 201


@auth
def warranties_get_all():
    warranties_query = db.session.query(Warranties).all()

    if len(warranties_query) == 0:
        return jsonify({"message": "no warranties were found"}), 404

    return jsonify({"message": "warranties found", "results": warranties_schema.dump(warranties_query)}), 200


@auth
def warranty_get_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": f"warranty does not exist"}), 404

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty_query)}), 200


@auth
def warranty_update(req, warranty_id):
    post_data = req.form if req.form else req.json

    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    populate_object(warranty_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200


@has_admin_permissions
def warranty_delete(request, warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": f"warranty with id {warranty_id} does not exist"}), 404

    try:
        db.session.delete(warranty_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete"}), 400

    return jsonify({"message": f"warranty with id {warranty_id} deleted", "deleted warranty": warranty_schema.dump(warranty_query)}), 200
