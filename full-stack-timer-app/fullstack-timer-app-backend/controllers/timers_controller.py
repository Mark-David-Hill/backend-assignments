from flask import jsonify, request as req

from db import db
from models.timers import Timers, timers_schema, timer_schema
from util.reflection import populate_object


def timer_add():
    post_data = req.form if req.form else req.json

    new_record = Timers.new_timer()

    populate_object(new_record, post_data)

    try:
        db.session.add(new_record)
        db.session.commit()
    except:
        db.session.rollback()

        return jsonify({"message": "could not add new timer"}), 400

    return jsonify({"message": "success", "result": timer_schema.dump(new_record)}), 201

def timer_update_by_id(timer_id):
    post_data = req.form if req.form else req.json

    timer_record = db.session.query(Timers).filter(Timers.timer_id == timer_id).first()

    populate_object(timer_record, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()

        return jsonify({"message": "could not update timer"}), 400

    return jsonify({"message": "success", "result": timer_schema.dump(timer_record)}), 200