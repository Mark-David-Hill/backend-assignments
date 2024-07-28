import uuid

from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Timers(db.Model):
    __tablename__ = "Timers"

    timer_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.DateTime)
    stop_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, name, start_time, stop_time, duration, active=True):
        self.name = name
        self.start_time = start_time
        self.stop_time = stop_time
        self.duration = duration
        self.active = active

    def new_timer():
        return Timers("", None, None, 0, True)


class TimersSchema(ma.Schema):
    class Meta:
        fields = ['timer_id', 'name', 'start_time', 'stop_time', 'duration', 'active']


timer_schema = TimersSchema()
timers_schema = TimersSchema(many=True)