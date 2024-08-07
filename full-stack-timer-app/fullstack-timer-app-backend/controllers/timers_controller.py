from datetime import datetime, timezone

from flask import jsonify, request as req

from db import db
from models.timers import Timers, timers_schema, timer_schema
from util.reflection import populate_object
# from lib.authenticaate import auth


# @auth
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


# @auth
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


# @auth
def timers_get_all():
    timer_records = db.session.query(Timers).all()

    if timer_records:
        return jsonify({"message": "timers found", "results": timers_schema.dump(timer_records)}), 200
    else:
        return jsonify({"message": "no timers found"}), 404
    
    

# @auth
def timer_get_by_id(timer_id):
    timer_record = db.session.query(Timers).filter(Timers.timer_id == timer_id).first()

    if timer_record:
        return jsonify({"message": "timer found", "result": timer_schema.dump(timer_record)}), 200
    else:
        return jsonify({"message": "timer not found"}), 404
    

# @auth
def timer_start(timer_id):
    timer_record = db.session.query(Timers).filter(Timers.timer_id == timer_id).first()

    current_time = datetime.now(timezone.utc)

    if timer_record.start_time is not None:
        timer_record.stop_time = None
    else:
        timer_record.start_time = current_time


    try:
        db.session.commit()
    except:
        db.session.rollback()

        return jsonify({"message": "could not update timer"}), 400

    return jsonify({"message": "success", "result": timer_schema.dump(timer_record)}), 200


# @auth
def timer_stop(timer_id):
    timer_record = db.session.query(Timers).filter(Timers.timer_id == timer_id).first()

    current_time = datetime.now(timezone.utc)

    timer_record.stop_time = current_time

    try:
        db.session.commit()
    except:
        db.session.rollback()

        return jsonify({"message": "could not update timer"}), 400

    return jsonify({"message": "success", "result": timer_schema.dump(timer_record)}), 200


# @auth
# def timer_delete(timer_id):
#     timer_record = db.session.query(Timers).filter(Timers.timer_id == timer_id).first()


#     try:
#         db.session.delete(timer_record)
#         db.session.commit()
#     except:
#         db.session.rollback()

#         return jsonify({"message": "could not delete timer"}), 400

#     return jsonify({"message": "success, timer was deleted"}), 200