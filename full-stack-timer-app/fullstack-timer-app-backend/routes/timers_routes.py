from flask import Blueprint

import controllers

timers = Blueprint('timers', __name__)

@timers.route("/timer", methods=["POST"])
def timer_add():
    return controllers.timer_add()


@timers.route("/timer/<timer_id>", methods=["PUT"])
def timer_update_by_id(timer_id):
    return controllers.timer_update_by_id(timer_id)