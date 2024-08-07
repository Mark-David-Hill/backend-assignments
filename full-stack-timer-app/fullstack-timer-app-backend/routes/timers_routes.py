from flask import Blueprint

import controllers

timers = Blueprint('timers', __name__)

@timers.route("/timer", methods=["POST"])
def timer_add():
    return controllers.timer_add()


@timers.route("/timer/<timer_id>", methods=["PUT"])
def timer_update_by_id(timer_id):
    return controllers.timer_update_by_id(timer_id)


@timers.route("/timers")
def timers_get_all():
    return controllers.timers_get_all()


@timers.route("/timer/<timer_id>")
def timer_get_by_id(timer_id):
    return controllers.timer_get_by_id(timer_id)


@timers.route("/timer/start/<timer_id>", methods=["PATCH"])
def timer_start(timer_id):
    return controllers.timer_start(timer_id)


@timers.route("/timer/stop/<timer_id>", methods=["PATCH"])
def timer_stop(timer_id):
    return controllers.timer_stop(timer_id)


@timers.route("/timer/delete/<timer_id>", methods=["DELETE"])
def timer_delete(timer_id):
    return controllers.timer_delete(timer_id)
